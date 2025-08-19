
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v3.0 - Massive Data Collector
Coleta massiva de dados antes das análises
"""

import os
import logging
import time
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
from services.enhanced_search_coordinator import enhanced_search_coordinator
from services.mcp_supadata_manager import mcp_supadata_manager
from services.alibaba_websailor import alibaba_websailor
from services.content_extractor import content_extractor
from services.production_search_manager import production_search_manager
from services.auto_save_manager import salvar_etapa

logger = logging.getLogger(__name__)

class MassiveDataCollector:
    """Coletor de dados massivo para criar JSON gigante"""

    def __init__(self):
        """Inicializa o coletor massivo"""
        self.collected_data = {}
        self.total_content_length = 0
        self.sources_count = 0
        
        logger.info("🚀 Massive Data Collector inicializado")

    def execute_massive_collection(
        self, 
        query: str, 
        context: Dict[str, Any], 
        session_id: str
    ) -> Dict[str, Any]:
        """Executa coleta massiva de dados de todas as fontes"""
        
        logger.info(f"🌊 INICIANDO COLETA MASSIVA DE DADOS para: {query}")
        start_time = time.time()
        
        # Estrutura do JSON gigante
        massive_data = {
            "metadata": {
                "session_id": session_id,
                "query": query,
                "context": context,
                "collection_started": datetime.now().isoformat(),
                "version": "ARQV30_Enhanced_v3.0"
            },
            "web_search_data": {},
            "social_media_data": {},
            "deep_navigation_data": {},
            "extracted_content": [],
            "statistics": {
                "total_sources": 0,
                "total_content_length": 0,
                "collection_time": 0,
                "sources_by_type": {}
            }
        }

        # FASE 1: Busca Web Massiva Simultânea
        logger.info("🔍 FASE 1: Executando busca web massiva...")
        web_data = self._execute_massive_web_search(query, context, session_id)
        massive_data["web_search_data"] = web_data
        
        # FASE 2: Coleta de Redes Sociais
        logger.info("📱 FASE 2: Executando coleta massiva de redes sociais...")
        social_data = self._execute_massive_social_collection(query, context, session_id)
        massive_data["social_media_data"] = social_data
        
        # FASE 3: Navegação Profunda
        logger.info("🌐 FASE 3: Executando navegação profunda...")
        deep_data = self._execute_deep_navigation(query, context, session_id)
        massive_data["deep_navigation_data"] = deep_data
        
        # FASE 4: Extração de Conteúdo Massiva
        logger.info("📄 FASE 4: Executando extração massiva de conteúdo...")
        extracted_data = self._execute_massive_content_extraction(massive_data, session_id)
        massive_data["extracted_content"] = extracted_data
        
        # Calcula estatísticas finais
        collection_time = time.time() - start_time
        self._calculate_final_statistics(massive_data, collection_time)
        
        # Salva JSON gigante
        self._save_massive_json(massive_data, session_id)
        
        logger.info(f"✅ COLETA MASSIVA CONCLUÍDA em {collection_time:.2f}s")
        logger.info(f"📊 Total de fontes: {massive_data['statistics']['total_sources']}")
        logger.info(f"📝 Total de conteúdo: {massive_data['statistics']['total_content_length']} caracteres")
        
        return massive_data

    def _execute_massive_web_search(self, query: str, context: Dict[str, Any], session_id: str) -> Dict[str, Any]:
        """Executa busca web massiva em todos os provedores"""
        
        web_search_data = {
            "enhanced_search_results": {},
            "production_search_results": {},
            "additional_queries_results": {}
        }
        
        # Busca principal com enhanced search coordinator
        try:
            main_results = enhanced_search_coordinator.execute_simultaneous_distinct_search(
                query, context, session_id
            )
            web_search_data["enhanced_search_results"] = main_results
        except Exception as e:
            logger.error(f"❌ Erro na busca enhanced: {e}")
            web_search_data["enhanced_search_results"] = {"error": str(e)}
        
        # Busca adicional com production search
        try:
            production_results = production_search_manager.search_with_fallback(query, max_results=50)
            web_search_data["production_search_results"] = {
                "results": production_results,
                "total": len(production_results)
            }
        except Exception as e:
            logger.error(f"❌ Erro na busca production: {e}")
            web_search_data["production_search_results"] = {"error": str(e)}
        
        # Queries adicionais baseadas no contexto
        additional_queries = self._generate_additional_queries(query, context)
        web_search_data["additional_queries_results"] = {}
        
        for additional_query in additional_queries:
            try:
                additional_results = production_search_manager.search_with_fallback(
                    additional_query, max_results=20
                )
                web_search_data["additional_queries_results"][additional_query] = {
                    "results": additional_results,
                    "total": len(additional_results)
                }
            except Exception as e:
                logger.error(f"❌ Erro na busca adicional '{additional_query}': {e}")
                web_search_data["additional_queries_results"][additional_query] = {"error": str(e)}
        
        return web_search_data

    def _execute_massive_social_collection(self, query: str, context: Dict[str, Any], session_id: str) -> Dict[str, Any]:
        """Executa coleta massiva de redes sociais"""
        
        social_data = {
            "all_platforms_data": {},
            "sentiment_analysis": {},
            "trending_topics": {},
            "engagement_metrics": {}
        }
        
        try:
            # Coleta em todas as plataformas
            platforms_results = mcp_supadata_manager.search_all_platforms(query, 25)
            social_data["all_platforms_data"] = platforms_results
            
            # Análise de sentimento
            all_posts = []
            for platform_name, platform_data in platforms_results.get('platforms', {}).items():
                if platform_data.get('results'):
                    all_posts.extend(platform_data['results'])
            
            if all_posts:
                sentiment_analysis = mcp_supadata_manager.analyze_sentiment_trends(platforms_results)
                social_data["sentiment_analysis"] = sentiment_analysis
            
            # Análise de engajamento e trending
            social_data["engagement_metrics"] = self._analyze_social_engagement(platforms_results)
            social_data["trending_topics"] = self._extract_trending_topics(all_posts)
            
        except Exception as e:
            logger.error(f"❌ Erro na coleta social: {e}")
            social_data["error"] = str(e)
        
        return social_data

    def _execute_deep_navigation(self, query: str, context: Dict[str, Any], session_id: str) -> Dict[str, Any]:
        """Executa navegação profunda com Alibaba WebSailor"""
        
        deep_data = {
            "websailor_navigation": {},
            "deep_content_analysis": {},
            "quality_metrics": {}
        }
        
        try:
            # Navegação profunda
            websailor_results = alibaba_websailor.navigate_and_research_deep(
                query, context, max_pages=50, depth_levels=4, session_id=session_id
            )
            deep_data["websailor_navigation"] = websailor_results
            
            # Análise de qualidade do conteúdo navegado
            if websailor_results.get('conteudo_consolidado'):
                deep_data["quality_metrics"] = self._analyze_content_quality(websailor_results)
            
        except Exception as e:
            logger.error(f"❌ Erro na navegação profunda: {e}")
            deep_data["error"] = str(e)
        
        return deep_data

    def _execute_massive_content_extraction(self, massive_data: Dict[str, Any], session_id: str) -> List[Dict[str, Any]]:
        """Executa extração massiva de conteúdo de todas as URLs coletadas"""
        
        all_urls = set()
        extracted_content = []
        
        # Coleta todas as URLs de todas as fontes
        self._collect_urls_from_web_search(massive_data["web_search_data"], all_urls)
        self._collect_urls_from_social_data(massive_data["social_media_data"], all_urls)
        self._collect_urls_from_deep_navigation(massive_data["deep_navigation_data"], all_urls)
        
        logger.info(f"🔗 Total de URLs para extração: {len(all_urls)}")
        
        # Extração paralela de conteúdo
        with ThreadPoolExecutor(max_workers=10) as executor:
            future_to_url = {
                executor.submit(self._extract_single_url_content, url): url 
                for url in list(all_urls)[:100]  # Limita a 100 URLs por performance
            }
            
            for future in as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    content_data = future.result(timeout=30)
                    if content_data and content_data.get('content'):
                        extracted_content.append(content_data)
                        logger.info(f"✅ Extraído: {url} ({len(content_data['content'])} chars)")
                except Exception as e:
                    logger.warning(f"⚠️ Erro ao extrair {url}: {e}")
        
        return extracted_content

    def _extract_single_url_content(self, url: str) -> Optional[Dict[str, Any]]:
        """Extrai conteúdo de uma única URL"""
        try:
            content = content_extractor.extract_content(url)
            if content and len(content) > 500:  # Mínimo de 500 caracteres
                return {
                    "url": url,
                    "content": content,
                    "length": len(content),
                    "extracted_at": datetime.now().isoformat(),
                    "extraction_method": "content_extractor"
                }
        except Exception as e:
            logger.debug(f"Erro ao extrair {url}: {e}")
        return None

    def _collect_urls_from_web_search(self, web_data: Dict[str, Any], all_urls: set):
        """Coleta URLs dos dados de busca web"""
        try:
            # Enhanced search results
            enhanced_results = web_data.get("enhanced_search_results", {})
            for provider_results in ["exa_results", "google_results", "other_results"]:
                results = enhanced_results.get(provider_results, [])
                for result in results:
                    if result.get("url"):
                        all_urls.add(result["url"])
            
            # Production search results
            production_results = web_data.get("production_search_results", {}).get("results", [])
            for result in production_results:
                if result.get("url"):
                    all_urls.add(result["url"])
            
            # Additional queries results
            additional_results = web_data.get("additional_queries_results", {})
            for query_results in additional_results.values():
                if isinstance(query_results, dict) and query_results.get("results"):
                    for result in query_results["results"]:
                        if result.get("url"):
                            all_urls.add(result["url"])
        except Exception as e:
            logger.error(f"❌ Erro ao coletar URLs web: {e}")

    def _collect_urls_from_social_data(self, social_data: Dict[str, Any], all_urls: set):
        """Coleta URLs dos dados de redes sociais"""
        try:
            platforms_data = social_data.get("all_platforms_data", {}).get("platforms", {})
            for platform_data in platforms_data.values():
                if platform_data.get("results"):
                    for post in platform_data["results"]:
                        if post.get("url"):
                            all_urls.add(post["url"])
        except Exception as e:
            logger.error(f"❌ Erro ao coletar URLs sociais: {e}")

    def _collect_urls_from_deep_navigation(self, deep_data: Dict[str, Any], all_urls: set):
        """Coleta URLs da navegação profunda"""
        try:
            websailor_data = deep_data.get("websailor_navigation", {})
            conteudo_consolidado = websailor_data.get("conteudo_consolidado", {})
            fontes_detalhadas = conteudo_consolidado.get("fontes_detalhadas", [])
            
            for fonte in fontes_detalhadas:
                if fonte.get("url"):
                    all_urls.add(fonte["url"])
        except Exception as e:
            logger.error(f"❌ Erro ao coletar URLs navegação: {e}")

    def _generate_additional_queries(self, base_query: str, context: Dict[str, Any]) -> List[str]:
        """Gera queries adicionais baseadas no contexto"""
        additional_queries = []
        
        segmento = context.get("segmento", "")
        produto = context.get("produto", "")
        
        if segmento and produto:
            additional_queries.extend([
                f"{segmento} {produto} mercado brasileiro 2024",
                f"{segmento} {produto} concorrentes Brasil",
                f"{segmento} {produto} tendências futuro",
                f"como vender {produto} {segmento}",
                f"estratégias marketing {segmento} {produto}",
                f"público-alvo {segmento} {produto}",
                f"preços {produto} {segmento} Brasil",
                f"cases sucesso {segmento} {produto}"
            ])
        
        return additional_queries[:5]  # Limita a 5 queries adicionais

    def _analyze_social_engagement(self, platforms_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analisa métricas de engajamento das redes sociais"""
        engagement_metrics = {
            "total_posts": 0,
            "platforms_active": 0,
            "avg_engagement_score": 0,
            "top_performing_platforms": []
        }
        
        try:
            platforms = platforms_data.get("platforms", {})
            platform_scores = []
            
            for platform_name, platform_data in platforms.items():
                posts = platform_data.get("results", [])
                if posts:
                    engagement_metrics["total_posts"] += len(posts)
                    engagement_metrics["platforms_active"] += 1
                    
                    # Calcula score básico da plataforma
                    platform_score = len(posts) * 10  # Score simples baseado no número de posts
                    platform_scores.append({
                        "platform": platform_name,
                        "score": platform_score,
                        "posts_count": len(posts)
                    })
            
            # Ordena plataformas por score
            platform_scores.sort(key=lambda x: x["score"], reverse=True)
            engagement_metrics["top_performing_platforms"] = platform_scores[:3]
            
            if platform_scores:
                engagement_metrics["avg_engagement_score"] = sum(p["score"] for p in platform_scores) / len(platform_scores)
        
        except Exception as e:
            logger.error(f"❌ Erro na análise de engajamento: {e}")
            engagement_metrics["error"] = str(e)
        
        return engagement_metrics

    def _extract_trending_topics(self, all_posts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Extrai tópicos trending dos posts coletados"""
        trending_topics = {
            "keywords_frequency": {},
            "hashtags_found": [],
            "common_themes": []
        }
        
        try:
            all_text = []
            hashtags = []
            
            for post in all_posts:
                # Coleta texto dos posts
                post_text = ""
                if post.get("content"):
                    post_text += post["content"] + " "
                if post.get("title"):
                    post_text += post["title"] + " "
                if post.get("text"):
                    post_text += post["text"] + " "
                if post.get("caption"):
                    post_text += post["caption"] + " "
                
                if post_text.strip():
                    all_text.append(post_text.lower())
                
                # Coleta hashtags
                hashtags.extend(post.get("hashtags_detected", []))
            
            # Análise básica de palavras-chave
            if all_text:
                combined_text = " ".join(all_text)
                words = combined_text.split()
                word_freq = {}
                
                for word in words:
                    if len(word) > 3:  # Ignora palavras muito curtas
                        word_freq[word] = word_freq.get(word, 0) + 1
                
                # Top 20 palavras mais frequentes
                sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
                trending_topics["keywords_frequency"] = dict(sorted_words[:20])
            
            # Hashtags únicas
            trending_topics["hashtags_found"] = list(set(hashtags))[:10]
            
            # Temas comuns (básico)
            common_themes = []
            if trending_topics["keywords_frequency"]:
                top_words = list(trending_topics["keywords_frequency"].keys())[:10]
                for i in range(0, len(top_words), 2):
                    if i + 1 < len(top_words):
                        theme = f"{top_words[i]} + {top_words[i+1]}"
                        common_themes.append(theme)
            
            trending_topics["common_themes"] = common_themes[:5]
        
        except Exception as e:
            logger.error(f"❌ Erro na extração de trending topics: {e}")
            trending_topics["error"] = str(e)
        
        return trending_topics

    def _analyze_content_quality(self, websailor_results: Dict[str, Any]) -> Dict[str, Any]:
        """Analisa qualidade do conteúdo navegado"""
        quality_metrics = {
            "content_depth_score": 0,
            "source_reliability_score": 0,
            "information_richness": 0,
            "total_insights": 0
        }
        
        try:
            conteudo_consolidado = websailor_results.get("conteudo_consolidado", {})
            
            # Score de profundidade baseado em insights
            insights = conteudo_consolidado.get("insights_principais", [])
            quality_metrics["total_insights"] = len(insights)
            quality_metrics["content_depth_score"] = min(len(insights) * 10, 100)
            
            # Score de confiabilidade baseado nas fontes
            fontes = conteudo_consolidado.get("fontes_detalhadas", [])
            if fontes:
                avg_quality = sum(fonte.get("quality_score", 0) for fonte in fontes) / len(fontes)
                quality_metrics["source_reliability_score"] = avg_quality
            
            # Score de riqueza de informação baseado no tamanho do conteúdo
            navegacao_profunda = websailor_results.get("navegacao_profunda", {})
            total_chars = navegacao_profunda.get("total_caracteres_analisados", 0)
            quality_metrics["information_richness"] = min(total_chars / 1000, 100)  # Normaliza para 0-100
        
        except Exception as e:
            logger.error(f"❌ Erro na análise de qualidade: {e}")
            quality_metrics["error"] = str(e)
        
        return quality_metrics

    def _calculate_final_statistics(self, massive_data: Dict[str, Any], collection_time: float):
        """Calcula estatísticas finais da coleta"""
        stats = massive_data["statistics"]
        
        # Conta fontes por tipo
        stats["sources_by_type"] = {
            "web_search": 0,
            "social_media": 0,
            "deep_navigation": 0,
            "extracted_content": len(massive_data["extracted_content"])
        }
        
        # Conta fontes de busca web
        web_data = massive_data["web_search_data"]
        enhanced_results = web_data.get("enhanced_search_results", {})
        stats["sources_by_type"]["web_search"] += len(enhanced_results.get("exa_results", []))
        stats["sources_by_type"]["web_search"] += len(enhanced_results.get("google_results", []))
        stats["sources_by_type"]["web_search"] += len(enhanced_results.get("other_results", []))
        
        production_results = web_data.get("production_search_results", {})
        stats["sources_by_type"]["web_search"] += len(production_results.get("results", []))
        
        # Conta fontes de redes sociais
        social_data = massive_data["social_media_data"]
        platforms_data = social_data.get("all_platforms_data", {}).get("platforms", {})
        for platform_data in platforms_data.values():
            stats["sources_by_type"]["social_media"] += len(platform_data.get("results", []))
        
        # Conta fontes de navegação profunda
        deep_data = massive_data["deep_navigation_data"]
        websailor_data = deep_data.get("websailor_navigation", {})
        fontes = websailor_data.get("conteudo_consolidado", {}).get("fontes_detalhadas", [])
        stats["sources_by_type"]["deep_navigation"] = len(fontes)
        
        # Total de fontes
        stats["total_sources"] = sum(stats["sources_by_type"].values())
        
        # Total de caracteres de conteúdo extraído
        total_chars = 0
        for content_item in massive_data["extracted_content"]:
            total_chars += content_item.get("length", 0)
        stats["total_content_length"] = total_chars
        
        # Tempo de coleta
        stats["collection_time"] = collection_time
        
        # Metadados de finalização
        massive_data["metadata"]["collection_completed"] = datetime.now().isoformat()
        massive_data["metadata"]["collection_duration_seconds"] = collection_time

    def _save_massive_json(self, massive_data: Dict[str, Any], session_id: str):
        """Salva o JSON gigante"""
        try:
            # Salva usando auto_save_manager
            salvar_etapa("massive_data_collection", massive_data, categoria="massive_collections")
            
            # Também salva uma versão compacta para análise rápida
            compact_data = {
                "metadata": massive_data["metadata"],
                "statistics": massive_data["statistics"],
                "summary": {
                    "total_web_sources": massive_data["statistics"]["sources_by_type"]["web_search"],
                    "total_social_sources": massive_data["statistics"]["sources_by_type"]["social_media"],
                    "total_deep_sources": massive_data["statistics"]["sources_by_type"]["deep_navigation"],
                    "total_extracted_content": len(massive_data["extracted_content"]),
                    "total_content_length": massive_data["statistics"]["total_content_length"]
                }
            }
            
            salvar_etapa("massive_data_summary", compact_data, categoria="massive_collections")
            
            logger.info("✅ JSON gigante salvo com sucesso")
            
        except Exception as e:
            logger.error(f"❌ Erro ao salvar JSON gigante: {e}")

# Instância global
massive_data_collector = MassiveDataCollector()
