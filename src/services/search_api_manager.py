#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v3.0 - Search API Manager ULTRA-ROBUSTO
Gerenciador de rotação de chaves com Alibaba WebSailor e busca social massiva
"""

import os
import logging
import asyncio
import time
from typing import Dict, List, Optional, Any
from datetime import datetime
from services.alibaba_websailor import alibaba_websailor
from services.viral_content_analyzer import viral_content_analyzer

logger = logging.getLogger(__name__)

class SearchAPIManager:
    """Gerenciador ULTRA-ROBUSTO com Alibaba WebSailor e busca social"""

    def __init__(self):
        """Inicializa o gerenciador com rotação de chaves"""
        self.api_keys: Dict[str, List[str]] = {}
        self.key_indices: Dict[str, int] = {}
        self.providers = ['FIRECRAWL', 'JINA', 'GOOGLE', 'EXA', 'SERPER', 'YOUTUBE']
        
        # Configuração do Alibaba WebSailor
        self.websailor_enabled = True
        self.social_search_enabled = True
        self.screenshot_capture_enabled = True

        self._load_api_keys()
        logger.info(f"🚀 Search API Manager ULTRA-ROBUSTO inicializado")
        logger.info(f"🔑 {sum(len(keys) for keys in self.api_keys.values())} chaves de API carregadas")
        logger.info(f"🌐 Alibaba WebSailor: {'✅ ATIVO' if self.websailor_enabled else '❌ INATIVO'}")
        logger.info(f"📱 Busca Social: {'✅ ATIVA' if self.social_search_enabled else '❌ INATIVA'}")
        logger.info(f"📸 Screenshots: {'✅ ATIVOS' if self.screenshot_capture_enabled else '❌ INATIVOS'}")

    def _load_api_keys(self):
        """Carrega todas as chaves de API do ambiente"""
        for provider in self.providers:
            keys = []

            # Carrega chave principal
            main_key = os.getenv(f"{provider}_API_KEY")
            if main_key:
                keys.append(main_key)

            # Carrega chaves numeradas (1, 2, 3, etc.)
            counter = 1
            while True:
                numbered_key = os.getenv(f"{provider}_API_KEY_{counter}")
                if numbered_key:
                    keys.append(numbered_key)
                    counter += 1
                else:
                    break

            if keys:
                self.api_keys[provider] = keys
                self.key_indices[provider] = 0
                logger.info(f"✅ {provider}: {len(keys)} chaves carregadas")
            elif provider in ['GOOGLE', 'YOUTUBE']:
                logger.info(f"ℹ️ {provider}: Chave opcional não configurada")
            else:
                logger.warning(f"⚠️ {provider}: Nenhuma chave encontrada")

    def get_next_key(self, provider: str) -> Optional[str]:
        """Retorna a próxima chave de API disponível para um provedor"""
        if provider not in self.api_keys or not self.api_keys[provider]:
            logger.warning(f"⚠️ Nenhuma chave disponível para {provider}")
            return None

        keys = self.api_keys[provider]
        current_index = self.key_indices[provider]

        # Obtém a chave atual
        key = keys[current_index]

        # Rotaciona para a próxima chave
        self.key_indices[provider] = (current_index + 1) % len(keys)

        logger.debug(f"🔄 {provider}: Usando chave {current_index + 1}/{len(keys)}")
        return key

    async def execute_massive_search_with_websailor(
        self, 
        query: str, 
        context: Dict[str, Any],
        session_id: str
    ) -> Dict[str, Any]:
        """Executa busca massiva com Alibaba WebSailor + APIs + Social"""
        
        logger.info(f"🚀 INICIANDO BUSCA MASSIVA ULTRA-ROBUSTA para: {query}")
        start_time = time.time()
        
        search_results = {
            'query': query,
            'session_id': session_id,
            'search_started': datetime.now().isoformat(),
            'websailor_results': {},
            'api_results': {},
            'social_results': {},
            'viral_content': [],
            'screenshots_captured': [],
            'statistics': {
                'total_sources': 0,
                'websailor_pages': 0,
                'api_sources': 0,
                'social_posts': 0,
                'screenshots_count': 0,
                'search_duration': 0
            }
        }
        
        try:
            # FASE 1: ALIBABA WEBSAILOR - NAVEGAÇÃO PROFUNDA
            logger.info("🌐 FASE 1: Executando Alibaba WebSailor - Navegação Profunda")
            if self.websailor_enabled:
                websailor_results = alibaba_websailor.navigate_and_research_deep(
                    query=query,
                    context=context,
                    max_pages=50,
                    depth_levels=4,
                    session_id=session_id
                )
                search_results['websailor_results'] = websailor_results
                search_results['statistics']['websailor_pages'] = len(
                    websailor_results.get('conteudo_consolidado', {}).get('fontes_detalhadas', [])
                )
                logger.info(f"✅ WebSailor: {search_results['statistics']['websailor_pages']} páginas analisadas")
            
            # FASE 2: BUSCA COM ROTAÇÃO DE APIs
            logger.info("🔄 FASE 2: Executando busca com rotação de APIs")
            api_results = await self._execute_api_rotation_search(query)
            search_results['api_results'] = api_results
            search_results['statistics']['api_sources'] = sum(
                len(result.get('results', [])) for result in api_results.values()
            )
            
            # FASE 3: BUSCA SOCIAL MASSIVA
            logger.info("📱 FASE 3: Executando busca social massiva")
            if self.social_search_enabled:
                social_results = await self._execute_social_search(query, context, session_id)
                search_results['social_results'] = social_results
                search_results['statistics']['social_posts'] = len(
                    social_results.get('all_posts', [])
                )
                
                # FASE 4: IDENTIFICAÇÃO E CAPTURA DE CONTEÚDO VIRAL
                logger.info("🔥 FASE 4: Identificando e capturando conteúdo viral")
                viral_content = self._identify_viral_content(social_results)
                search_results['viral_content'] = viral_content
                
                # FASE 5: SCREENSHOTS DOS POSTS MAIS VIRAIS
                if self.screenshot_capture_enabled and viral_content:
                    logger.info("📸 FASE 5: Capturando screenshots dos posts virais")
                    screenshots = await viral_content_analyzer.analyze_and_capture_viral_content(
                        search_results={'social_results': viral_content},
                        session_id=session_id,
                        max_captures=15
                    )
                    search_results['screenshots_captured'] = screenshots.get('screenshots_captured', [])
                    search_results['statistics']['screenshots_count'] = len(search_results['screenshots_captured'])
            
            # Calcula estatísticas finais
            search_duration = time.time() - start_time
            search_results['statistics']['search_duration'] = search_duration
            search_results['statistics']['total_sources'] = (
                search_results['statistics']['websailor_pages'] +
                search_results['statistics']['api_sources'] +
                search_results['statistics']['social_posts']
            )
            
            logger.info(f"✅ BUSCA MASSIVA CONCLUÍDA em {search_duration:.2f}s")
            logger.info(f"📊 Total: {search_results['statistics']['total_sources']} fontes")
            logger.info(f"📸 Screenshots: {search_results['statistics']['screenshots_count']}")
            
            return search_results
            
        except Exception as e:
            logger.error(f"❌ ERRO CRÍTICO na busca massiva: {e}")
            raise
    
    async def _execute_api_rotation_search(self, query: str) -> Dict[str, Any]:
        """Executa busca com rotação de APIs"""
        api_results = {}
        
        # Busca intercalada com rotação
        for provider in self.providers:
            if provider in self.api_keys:
                try:
                    api_key = self.get_next_key(provider)
                    if api_key:
                        logger.info(f"🔍 Buscando com {provider}...")
                        
                        if provider == 'GOOGLE':
                            result = await self._search_google(query, api_key)
                        elif provider == 'JINA':
                            result = await self._search_jina(query, api_key)
                        elif provider == 'EXA':
                            result = await self._search_exa(query, api_key)
                        elif provider == 'FIRECRAWL':
                            result = await self._search_firecrawl(query, api_key)
                        elif provider == 'SERPER':
                            result = await self._search_serper(query, api_key)
                        elif provider == 'YOUTUBE':
                            result = await self._search_youtube(query, api_key)
                        else:
                            continue
                        
                        api_results[provider] = result
                        
                        # Pequeno delay entre APIs
                        await asyncio.sleep(0.5)
                        
                except Exception as e:
                    logger.error(f"❌ Erro em {provider}: {e}")
                    api_results[provider] = {'success': False, 'error': str(e)}
        
        return api_results
    
    async def _execute_social_search(self, query: str, context: Dict[str, Any], session_id: str) -> Dict[str, Any]:
        """Executa busca social massiva"""
        try:
            from services.mcp_supadata_manager import mcp_supadata_manager
            
            # Busca em todas as plataformas sociais
            social_platforms = ['youtube', 'instagram', 'twitter', 'tiktok', 'facebook']
            all_posts = []
            platform_results = {}
            
            for platform in social_platforms:
                try:
                    logger.info(f"📱 Buscando em {platform}...")
                    
                    # Usa MCP Supadata para busca social
                    platform_data = mcp_supadata_manager.search_all_platforms(
                        query, max_results_per_platform=25
                    )
                    
                    if platform_data.get('success'):
                        platform_posts = platform_data.get('platforms', {}).get(platform, {}).get('results', [])
                        all_posts.extend(platform_posts)
                        platform_results[platform] = platform_posts
                        
                        logger.info(f"✅ {platform}: {len(platform_posts)} posts encontrados")
                    
                    await asyncio.sleep(0.3)  # Rate limiting
                    
                except Exception as e:
                    logger.error(f"❌ Erro em {platform}: {e}")
                    platform_results[platform] = []
            
            return {
                'all_posts': all_posts,
                'platform_results': platform_results,
                'total_posts': len(all_posts),
                'platforms_searched': social_platforms
            }
            
        except Exception as e:
            logger.error(f"❌ Erro na busca social: {e}")
            return {'all_posts': [], 'platform_results': {}, 'error': str(e)}
    
    def _identify_viral_content(self, social_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identifica conteúdo viral para screenshots"""
        all_posts = social_results.get('all_posts', [])
        
        if not all_posts:
            return []
        
        # Calcula score viral para cada post
        viral_posts = []
        
        for post in all_posts:
            viral_score = self._calculate_viral_score(post)
            
            if viral_score >= 6.0:  # Threshold para conteúdo viral
                post['viral_score'] = viral_score
                post['viral_category'] = self._categorize_viral_level(viral_score)
                viral_posts.append(post)
        
        # Ordena por score viral e retorna top 15
        viral_posts.sort(key=lambda x: x.get('viral_score', 0), reverse=True)
        
        logger.info(f"🔥 {len(viral_posts)} posts virais identificados")
        return viral_posts[:15]
    
    def _calculate_viral_score(self, post: Dict[str, Any]) -> float:
        """Calcula score viral baseado na plataforma"""
        platform = post.get('platform', 'unknown')
        
        try:
            if platform == 'youtube':
                views = int(post.get('view_count', post.get('views', 0)))
                likes = int(post.get('like_count', post.get('likes', 0)))
                comments = int(post.get('comment_count', post.get('comments', 0)))
                
                # Fórmula YouTube: views/1000 + likes/100 + comments/10
                score = (views / 1000) + (likes / 100) + (comments / 10)
                return min(10.0, score / 100)
                
            elif platform in ['instagram', 'facebook']:
                likes = int(post.get('likes', post.get('like_count', 0)))
                comments = int(post.get('comments', post.get('comment_count', 0)))
                shares = int(post.get('shares', 0))
                
                # Fórmula Instagram/Facebook
                score = (likes / 100) + (comments / 10) + (shares / 5)
                return min(10.0, score / 50)
                
            elif platform == 'twitter':
                retweets = int(post.get('retweets', post.get('retweet_count', 0)))
                likes = int(post.get('likes', post.get('like_count', 0)))
                replies = int(post.get('replies', post.get('reply_count', 0)))
                
                # Fórmula Twitter
                score = (retweets / 10) + (likes / 50) + (replies / 5)
                return min(10.0, score / 20)
                
            elif platform == 'tiktok':
                views = int(post.get('views', post.get('view_count', 0)))
                likes = int(post.get('likes', 0))
                shares = int(post.get('shares', 0))
                
                # Fórmula TikTok
                score = (views / 10000) + (likes / 500) + (shares / 100)
                return min(10.0, score / 50)
                
            else:
                # Score baseado em relevância para outros tipos
                return post.get('relevance_score', 0) * 10
                
        except (ValueError, TypeError):
            return 0.0
    
    def _categorize_viral_level(self, viral_score: float) -> str:
        """Categoriza nível viral"""
        if viral_score >= 9.0:
            return 'MEGA_VIRAL'
        elif viral_score >= 7.5:
            return 'VIRAL'
        elif viral_score >= 6.0:
            return 'TRENDING'
        else:
            return 'POPULAR'
    
    # Métodos de busca específicos (implementação simplificada)
    async def _search_google(self, query: str, api_key: str) -> Dict[str, Any]:
        """Busca Google com chave rotativa"""
        try:
            import aiohttp
            cx_id = os.getenv('GOOGLE_CSE_ID')
            if not cx_id:
                return {'provider': 'GOOGLE', 'success': False, 'error': 'CSE_ID não configurado'}
            
            async with aiohttp.ClientSession() as session:
                params = {
                    'key': api_key,
                    'cx': cx_id,
                    'q': f"{query} Brasil 2024",
                    'num': 10,
                    'lr': 'lang_pt',
                    'gl': 'br'
                }
                
                async with session.get(
                    'https://www.googleapis.com/customsearch/v1',
                    params=params,
                    timeout=30
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            'provider': 'GOOGLE',
                            'results': data.get('items', []),
                            'success': True
                        }
                    else:
                        return {'provider': 'GOOGLE', 'success': False, 'error': f'Status {response.status}'}
        except Exception as e:
            logger.error(f"❌ Google: {e}")
            return {'provider': 'GOOGLE', 'success': False, 'error': str(e)}
    
    async def _search_jina(self, query: str, api_key: str) -> Dict[str, Any]:
        """Busca Jina com chave rotativa"""
        try:
            import aiohttp
            async with aiohttp.ClientSession() as session:
                headers = {'Authorization': f'Bearer {api_key}'}
                search_url = f"https://r.jina.ai/https://www.google.com/search?q={query}"
                
                async with session.get(search_url, headers=headers, timeout=30) as response:
                    if response.status == 200:
                        content = await response.text()
                        return {
                            'provider': 'JINA',
                            'results': [{'content': content[:1000], 'url': search_url}],
                            'success': True
                        }
                    else:
                        return {'provider': 'JINA', 'success': False, 'error': f'Status {response.status}'}
        except Exception as e:
            return {'provider': 'JINA', 'success': False, 'error': str(e)}
    
    async def _search_exa(self, query: str, api_key: str) -> Dict[str, Any]:
        """Busca Exa com chave rotativa"""
        try:
            import aiohttp
            async with aiohttp.ClientSession() as session:
                headers = {'x-api-key': api_key, 'Content-Type': 'application/json'}
                payload = {'query': query, 'numResults': 10, 'type': 'neural'}
                
                async with session.post(
                    'https://api.exa.ai/search',
                    json=payload,
                    headers=headers,
                    timeout=30
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            'provider': 'EXA',
                            'results': data.get('results', []),
                            'success': True
                        }
                    else:
                        return {'provider': 'EXA', 'success': False, 'error': f'Status {response.status}'}
        except Exception as e:
            return {'provider': 'EXA', 'success': False, 'error': str(e)}
    
    async def _search_firecrawl(self, query: str, api_key: str) -> Dict[str, Any]:
        """Busca Firecrawl com chave rotativa"""
        try:
            import aiohttp
            async with aiohttp.ClientSession() as session:
                headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}
                payload = {
                    'url': f'https://www.google.com/search?q={query}',
                    'formats': ['markdown'],
                    'onlyMainContent': True
                }
                
                async with session.post(
                    'https://api.firecrawl.dev/v0/scrape',
                    json=payload,
                    headers=headers,
                    timeout=30
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        content = data.get('data', {}).get('markdown', '')
                        return {
                            'provider': 'FIRECRAWL',
                            'results': [{'content': content, 'url': payload['url']}],
                            'success': True
                        }
                    else:
                        return {'provider': 'FIRECRAWL', 'success': False, 'error': f'Status {response.status}'}
        except Exception as e:
            return {'provider': 'FIRECRAWL', 'success': False, 'error': str(e)}
    
    async def _search_serper(self, query: str, api_key: str) -> Dict[str, Any]:
        """Busca Serper com chave rotativa"""
        try:
            import aiohttp
            async with aiohttp.ClientSession() as session:
                headers = {'X-API-KEY': api_key, 'Content-Type': 'application/json'}
                payload = {'q': query, 'gl': 'br', 'hl': 'pt', 'num': 10}
                
                async with session.post(
                    'https://google.serper.dev/search',
                    json=payload,
                    headers=headers,
                    timeout=30
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            'provider': 'SERPER',
                            'results': data.get('organic', []),
                            'success': True
                        }
                    else:
                        return {'provider': 'SERPER', 'success': False, 'error': f'Status {response.status}'}
        except Exception as e:
            return {'provider': 'SERPER', 'success': False, 'error': str(e)}
    
    async def _search_youtube(self, query: str, api_key: str) -> Dict[str, Any]:
        """Busca YouTube com chave rotativa"""
        try:
            import aiohttp
            async with aiohttp.ClientSession() as session:
                params = {
                    'part': 'snippet,statistics',
                    'q': f"{query} Brasil",
                    'key': api_key,
                    'maxResults': 25,
                    'order': 'viewCount',
                    'type': 'video'
                }
                
                async with session.get(
                    'https://www.googleapis.com/youtube/v3/search',
                    params=params,
                    timeout=30
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            'provider': 'YOUTUBE',
                            'results': data.get('items', []),
                            'success': True
                        }
                    else:
                        return {'provider': 'YOUTUBE', 'success': False, 'error': f'Status {response.status}'}
        except Exception as e:
            return {'provider': 'YOUTUBE', 'success': False, 'error': str(e)}
    
    # Método de compatibilidade
    async def interleaved_search(self, query: str) -> Dict[str, Any]:
        """Método de compatibilidade - redireciona para busca massiva"""
        context = {'query_original': query}
        session_id = f"search_{int(time.time())}"
        
        return await self.execute_massive_search_with_websailor(query, context, session_id)

    def get_available_providers(self) -> List[str]:
        """Retorna lista de provedores disponíveis"""
        return list(self.api_keys.keys())

    def get_provider_stats(self) -> Dict[str, Dict[str, Any]]:
        """Retorna estatísticas dos provedores"""
        stats = {}
        for provider in self.providers:
            if provider in self.api_keys:
                stats[provider] = {
                    'total_keys': len(self.api_keys[provider]),
                    'current_index': self.key_indices[provider],
                    'available': True
                }
            else:
                stats[provider] = {
                    'total_keys': 0,
                    'current_index': 0,
                    'available': False
                }
        return stats

# Instância global
search_api_manager = SearchAPIManager()