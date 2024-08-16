from graphrag.query.structured_search.global_search.community_context import GlobalCommunityContext
from graphrag.query.structured_search.global_search.search import GlobalSearch
from graphrag.query.structured_search.local_search.mixed_context import LocalSearchMixedContext
from graphrag.query.structured_search.local_search.search import LocalSearch
from graphrag.vector_stores.lancedb import LanceDBVectorStore
from graphrag.query.context_builder.entity_extraction import EntityVectorStoreKey
from graphrag.query.input.loaders.dfs import store_entity_semantic_embeddings
from graphrag.query.llm.oai.embedding import OpenAIEmbedding
from graphrag.query.llm.oai.typing import OpenaiApiType
from ..config import MAX_TOKENS_GLOBAL, MAX_TOKENS_LOCAL, TEMPERATURE, RESPONSE_TYPE, CONCURRENT_COROUTINES
import logging

logger = logging.getLogger(__name__)

def setup_global_search_engine(llm, token_encoder, reports, entities, context_builder_params, allow_general_knowledge):
    map_llm_params = {"max_tokens": 1000, "temperature": TEMPERATURE, "response_format": {"type": "json_object"}}
    reduce_llm_params = {"max_tokens": 2000, "temperature": TEMPERATURE}
    return GlobalSearch(
        llm=llm,
        context_builder=GlobalCommunityContext(community_reports=reports, entities=entities, token_encoder=token_encoder),
        token_encoder=token_encoder,
        max_data_tokens=MAX_TOKENS_GLOBAL,
        map_llm_params=map_llm_params,
        reduce_llm_params=reduce_llm_params,
        allow_general_knowledge=allow_general_knowledge,
        json_mode=True,
        context_builder_params=context_builder_params,
        concurrent_coroutines=CONCURRENT_COROUTINES,
        response_type=RESPONSE_TYPE
    )

def setup_local_search_engine(llm, token_encoder, reports, entities, relationships, covariates, text_units, env_vars, local_context_params):
    lancedb_uri = f"{env_vars['artifacts_dir']}/lancedb"
    description_embedding_store = LanceDBVectorStore(collection_name="entity_description_embeddings")
    description_embedding_store.connect(db_uri=lancedb_uri)
    
    text_embedder = OpenAIEmbedding(
        api_key=env_vars["api_key"],
        api_base=None,
        api_type=OpenaiApiType.OpenAI,
        model=env_vars["embedding_model"],
        deployment_name=env_vars["embedding_model"],
        max_retries=20,
    )
    
    entity_description_embeddings = store_entity_semantic_embeddings(
        entities=entities, vectorstore=description_embedding_store
    )
    
    context_builder = LocalSearchMixedContext(
        community_reports=reports,
        text_units=text_units,
        entities=entities,
        relationships=relationships,
        covariates=covariates,
        entity_text_embeddings=description_embedding_store,
        embedding_vectorstore_key=EntityVectorStoreKey.ID,
        text_embedder=text_embedder,
        token_encoder=token_encoder,
    )
    
    llm_params = {
        "max_tokens": MAX_TOKENS_LOCAL,
        "temperature": TEMPERATURE,
    }
    
    return LocalSearch(
        llm=llm,
        context_builder=context_builder,
        token_encoder=token_encoder,
        llm_params=llm_params,
        context_builder_params=local_context_params,
        response_type=RESPONSE_TYPE,
    )

def setup_search_engines(llm, token_encoder, reports, entities, relationships, covariates, text_units, env_vars, config):
    global_context_builder_params = {
        "use_community_summary": config["use_community_summary"],
        "shuffle_data": True,
        "include_community_rank": config["include_community_rank"],
        "min_community_rank": 0,
        "community_rank_name": "rank",
        "include_community_weight": True,
        "community_weight_name": "occurrence weight",
        "normalize_community_weight": True,
        "max_tokens": MAX_TOKENS_GLOBAL,
        "context_name": "Reports",
    }

    local_context_params = {
        "text_unit_prop": 0.5,
        "community_prop": 0.1,
        "conversation_history_max_turns": 5,
        "conversation_history_user_turns_only": True,
        "top_k_mapped_entities": 10,
        "top_k_relationships": 10,
        "include_entity_rank": True,
        "include_relationship_weight": True,
        "include_community_rank": config["include_community_rank"],
        "return_candidate_context": False,
        "embedding_vectorstore_key": EntityVectorStoreKey.ID,
        "max_tokens": MAX_TOKENS_GLOBAL,
    }

    global_search_engine = setup_global_search_engine(llm, token_encoder, reports, entities, global_context_builder_params, config["allow_general_knowledge"])
    local_search_engine = setup_local_search_engine(llm, token_encoder, reports, entities, relationships, covariates, text_units, env_vars, local_context_params)

    return global_search_engine, local_search_engine