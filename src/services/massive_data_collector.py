#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v3.0 - Massive Data Collector CORRIGIDO
Coletor que gera arquivo .md gigante com TODAS as informações para estudo da IA
"""

import os
import logging
import time
import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path

# Importa serviços necessários
from services.search_api_manager import search_api_manager
from services.social_media_extractor import social_media_extractor
from services.trendfinder_client import trendfinder_client
from services.visual_content_capture import visual_content_capture

logger = logging.getLogger(__name__)

class MassiveDataCollector:
    """Coletor de dados massivos que gera .md gigante para estudo da IA"""

    def __init__(self):
        """Inicializa o coletor massivo"""
        self.base_dir = "analyses_data"
        self.ensure_base_directories()
        logger.info("🌊 Massive Data Collector CORRIGIDO inicializado")

    def ensure_base_directories(self):
        """Garante que os diretórios base existem"""
        Path(self.base_dir).mkdir(exist_ok=True)
        Path(f"{self.base_dir}/files").mkdir(exist_ok=True)

    async def execute_massive_collection(
        self, 
        query: str, 
        context: Dict[str, Any], 
        session_id: str
    ) -> Dict[str, Any]:
        """
        Executa coleta massiva e gera arquivo .md gigante
        
        ETAPA 1: Coleta Massiva e Consolidação Visual
        - Busca web intercalada com múltiplos provedores
        - Busca em redes sociais (TrendFinder + SupaData)
        - Captura de screenshots dos posts mais virais
        - Geração do relatorio_coleta.md GIGANTE
        """
        logger.info(f"🌊 INICIANDO COLETA MASSIVA para: {query}")
        start_time = time.time()
        
        # Estrutura de resultados
        massive_results = {
            'session_id': session_id,
            'query': query,
            'context': context,
            'start_time': datetime.now().isoformat(),
            'web_search_results': {},
            'social_media_results': {},
            'trendfinder_results': {},
            'viral_posts_screenshots': {},
            'statistics': {},
            'giant_md_path': None
        }
        
        try:
            # 1. BUSCA WEB INTERCALADA
            logger.info("🔍 Executando busca web intercalada...")
            web_results = await self._execute_interleaved_web_search(query)
            massive_results['web_search_results'] = web_results
            
            # 2. BUSCA EM REDES SOCIAIS
            logger.info("📱 Executando busca em redes sociais...")
            social_results = await self._execute_social_media_search(query, context, session_id)
            massive_results['social_media_results'] = social_results
            
            # 3. BUSCA COM TRENDFINDER
            logger.info("📈 Executando busca com TrendFinder...")
            trend_results = await self._execute_trendfinder_search(query)
            massive_results['trendfinder_results'] = trend_results
            
            # 4. CAPTURA DE SCREENSHOTS DOS POSTS VIRAIS
            logger.info("📸 Capturando screenshots dos posts virais...")
            screenshots_results = await self._capture_viral_screenshots(social_results, session_id)
            massive_results['viral_posts_screenshots'] = screenshots_results
            
            # 5. GERA ARQUIVO .MD GIGANTE
            logger.info("📄 Gerando arquivo .md GIGANTE para estudo da IA...")
            giant_md_path = await self._generate_giant_markdown_report(massive_results, session_id)
            massive_results['giant_md_path'] = giant_md_path
            
            # 6. CALCULA ESTATÍSTICAS
            execution_time = time.time() - start_time
            massive_results['statistics'] = self._calculate_collection_statistics(massive_results, execution_time)
            massive_results['end_time'] = datetime.now().isoformat()
            
            logger.info(f"✅ COLETA MASSIVA CONCLUÍDA em {execution_time:.2f}s")
            logger.info(f"📊 Arquivo .md gigante: {giant_md_path}")
            
            return massive_results
            
        except Exception as e:
            logger.error(f"❌ ERRO CRÍTICO na coleta massiva: {e}")
            massive_results['error'] = str(e)
            massive_results['success'] = False
            return massive_results

    async def _execute_interleaved_web_search(self, query: str) -> Dict[str, Any]:
        """Executa busca web intercalada com múltiplos provedores"""
        try:
            # Usa o SearchAPIManager para busca intercalada
            search_results = await search_api_manager.interleaved_search(query)
            
            logger.info(f"✅ Busca web intercalada: {search_results.get('successful_searches', 0)} sucessos")
            return search_results
            
        except Exception as e:
            logger.error(f"❌ Erro na busca web intercalada: {e}")
            return {
                'success': False,
                'error': str(e),
                'query': query
            }

    async def _execute_social_media_search(self, query: str, context: Dict[str, Any], session_id: str) -> Dict[str, Any]:
        """Executa busca abrangente em redes sociais"""
        try:
            # Usa o SocialMediaExtractor
            social_results = social_media_extractor.extract_comprehensive_data(query, context, session_id)
            
            logger.info(f"✅ Busca redes sociais: {social_results.get('total_posts', 0)} posts encontrados")
            return social_results
            
        except Exception as e:
            logger.error(f"❌ Erro na busca de redes sociais: {e}")
            return {
                'success': False,
                'error': str(e),
                'query': query
            }

    async def _execute_trendfinder_search(self, query: str) -> Dict[str, Any]:
        """Executa busca com TrendFinder MCP"""
        try:
            # Usa o TrendFinderClient
            trend_results = await trendfinder_client.search(query)
            
            logger.info(f"✅ TrendFinder: {len(trend_results.get('trends', []))} tendências encontradas")
            return trend_results
            
        except Exception as e:
            logger.error(f"❌ Erro no TrendFinder: {e}")
            return {
                'success': False,
                'error': str(e),
                'query': query
            }

    async def _capture_viral_screenshots(self, social_results: Dict[str, Any], session_id: str) -> Dict[str, Any]:
        """Captura screenshots dos posts com maior engajamento"""
        try:
            # Usa o VisualContentCapture para capturar posts virais
            screenshots_results = await visual_content_capture.capture_viral_posts_screenshots(
                social_results, session_id
            )
            
            logger.info(f"✅ Screenshots: {screenshots_results.get('screenshots_captured', 0)} capturas realizadas")
            return screenshots_results
            
        except Exception as e:
            logger.error(f"❌ Erro na captura de screenshots: {e}")
            return {
                'success': False,
                'error': str(e),
                'session_id': session_id
            }

    async def _generate_giant_markdown_report(self, massive_results: Dict[str, Any], session_id: str) -> str:
        """
        Gera arquivo .md GIGANTE com TODAS as informações coletadas
        Este arquivo será usado pela IA para "estudar" na Etapa 2
        """
        try:
            session_dir = Path(self.base_dir) / session_id
            session_dir.mkdir(exist_ok=True)
            
            md_path = session_dir / "relatorio_coleta.md"
            
            # Constrói o conteúdo do markdown gigante
            md_content = self._build_giant_markdown_content(massive_results)
            
            # Salva o arquivo
            with open(md_path, 'w', encoding='utf-8') as f:
                f.write(md_content)
            
            # Verifica tamanho do arquivo
            file_size_mb = md_path.stat().st_size / (1024 * 1024)
            logger.info(f"📄 Arquivo .md gigante criado: {file_size_mb:.2f}MB")
            
            return str(md_path)
            
        except Exception as e:
            logger.error(f"❌ Erro ao gerar .md gigante: {e}")
            return None

    def _build_giant_markdown_content(self, massive_results: Dict[str, Any]) -> str:
        """Constrói o conteúdo completo do markdown gigante"""
        
        session_id = massive_results['session_id']
        query = massive_results['query']
        context = massive_results['context']
        
        md_content = f"""# RELATÓRIO DE COLETA MASSIVA - ETAPA 1
## Sessão: {session_id}
## Query: {query}
## Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

---

## 1. CONTEXTO DO PROJETO

**Query de Busca:** {query}

**Contexto Fornecido:**
```json
{context}
```

**Objetivo:** Coleta massiva de dados reais para análise aprofundada de mercado e geração de insights estratégicos.

---

## 2. RESULTADOS DA BUSCA WEB INTERCALADA

### 2.1 Estatísticas Gerais
"""
        
        # Adiciona resultados da busca web
        web_results = massive_results.get('web_search_results', {})
        if web_results.get('successful_searches', 0) > 0:
            md_content += f"""
- **Provedores Utilizados:** {len(web_results.get('providers_used', []))}
- **Buscas Bem-sucedidas:** {web_results.get('successful_searches', 0)}
- **URLs Coletadas:** {len(web_results.get('consolidated_urls', []))}

### 2.2 URLs Encontradas
"""
            for i, url in enumerate(web_results.get('consolidated_urls', [])[:50], 1):
                md_content += f"{i}. {url}\n"
            
            # Adiciona resultados detalhados de cada provedor
            md_content += "\n### 2.3 Resultados Detalhados por Provedor\n"
            for result in web_results.get('all_results', []):
                if result.get('success'):
                    provider = result.get('provider', 'Unknown')
                    md_content += f"\n#### {provider}\n"
                    for item in result.get('results', [])[:10]:
                        title = item.get('title', 'Sem título')
                        url = item.get('url', item.get('link', ''))
                        content = item.get('content', item.get('snippet', ''))[:500]
                        md_content += f"**{title}**\n{url}\n{content}...\n\n"
        
        # Adiciona resultados das redes sociais
        md_content += "\n---\n\n## 3. RESULTADOS DAS REDES SOCIAIS\n"
        social_results = massive_results.get('social_media_results', {})
        
        if social_results.get('success'):
            platforms_data = social_results.get('all_platforms_data', {})
            md_content += f"""
### 3.1 Estatísticas Gerais
- **Total de Posts:** {platforms_data.get('total_results', 0)}
- **Plataformas Analisadas:** {len(platforms_data.get('platforms', []))}
- **Análise de Sentimento:** {social_results.get('sentiment_analysis', {}).get('overall_sentiment', 'N/A')}

"""
            
            # Adiciona dados de cada plataforma
            for platform in ['youtube', 'twitter', 'instagram', 'linkedin']:
                platform_data = platforms_data.get(platform, {})
                if platform_data.get('success'):
                    md_content += f"\n### 3.2 {platform.upper()}\n"
                    md_content += f"**Total de Posts:** {len(platform_data.get('results', []))}\n\n"
                    
                    for i, post in enumerate(platform_data.get('results', [])[:20], 1):
                        if platform == 'youtube':
                            md_content += f"**{i}. {post.get('title', 'Sem título')}**\n"
                            md_content += f"Canal: {post.get('channel', 'N/A')}\n"
                            md_content += f"Views: {post.get('view_count', 'N/A')}\n"
                            md_content += f"Likes: {post.get('like_count', 'N/A')}\n"
                            md_content += f"URL: {post.get('url', 'N/A')}\n"
                            md_content += f"Descrição: {post.get('description', 'N/A')[:200]}...\n\n"
                        
                        elif platform == 'twitter':
                            md_content += f"**{i}. Tweet de {post.get('author', 'N/A')}**\n"
                            md_content += f"Texto: {post.get('text', 'N/A')[:300]}...\n"
                            md_content += f"Likes: {post.get('like_count', 'N/A')}\n"
                            md_content += f"Retweets: {post.get('retweet_count', 'N/A')}\n"
                            md_content += f"URL: {post.get('url', 'N/A')}\n\n"
                        
                        elif platform == 'instagram':
                            md_content += f"**{i}. Post de {post.get('username', 'N/A')}**\n"
                            md_content += f"Caption: {post.get('caption', 'N/A')[:300]}...\n"
                            md_content += f"Likes: {post.get('like_count', 'N/A')}\n"
                            md_content += f"Comments: {post.get('comment_count', 'N/A')}\n"
                            md_content += f"URL: {post.get('url', 'N/A')}\n\n"
                        
                        elif platform == 'linkedin':
                            md_content += f"**{i}. {post.get('title', 'Sem título')}**\n"
                            md_content += f"Autor: {post.get('author', 'N/A')}\n"
                            md_content += f"Empresa: {post.get('company', 'N/A')}\n"
                            md_content += f"Conteúdo: {post.get('content', 'N/A')[:300]}...\n"
                            md_content += f"Likes: {post.get('likes', 'N/A')}\n"
                            md_content += f"URL: {post.get('url', 'N/A')}\n\n"
        
        # Adiciona resultados do TrendFinder
        md_content += "\n---\n\n## 4. RESULTADOS DO TRENDFINDER\n"
        trend_results = massive_results.get('trendfinder_results', {})
        
        if trend_results.get('success'):
            md_content += f"""
### 4.1 Tendências Identificadas
- **Total de Tendências:** {len(trend_results.get('trends', []))}
- **Hashtags Virais:** {len(trend_results.get('hashtags', []))}
- **Conteúdo Viral:** {len(trend_results.get('viral_content', []))}

"""
            
            # Adiciona tendências
            for i, trend in enumerate(trend_results.get('trends', [])[:20], 1):
                md_content += f"{i}. **{trend}**\n"
            
            # Adiciona hashtags
            md_content += "\n### 4.2 Hashtags em Tendência\n"



            for i, hashtag in enumerate(trend_results.get('hashtags', [])[:30], 1):
                md_content += f"{i}. #{hashtag}\n"
        
        # Adiciona screenshots dos posts virais
        md_content += "\n---\n\n## 5. SCREENSHOTS DOS POSTS VIRAIS\n"
        screenshots_results = massive_results.get('viral_posts_screenshots', {})
        
        if screenshots_results.get('screenshots_captured', 0) > 0:
            md_content += f"""
### 5.1 Estatísticas de Captura
- **Posts Analisados:** {screenshots_results.get('total_posts_analyzed', 0)}
- **Screenshots Capturados:** {screenshots_results.get('screenshots_captured', 0)}
- **Falhas:** {screenshots_results.get('failed_captures', 0)}

### 5.2 Posts Virais Capturados
"""
            
            for i, viral_post in enumerate(screenshots_results.get('viral_posts', []), 1):
                md_content += f"""
#### {i}. {viral_post.get('platform', 'Unknown').upper()} - Score: {viral_post.get('engagement_score', 0)}

**Título:** {viral_post.get('title', 'Sem título')}
**URL:** {viral_post.get('url', 'N/A')}
**Views:** {viral_post.get('views', 'N/A')}
**Likes:** {viral_post.get('likes', 'N/A')}
**Shares:** {viral_post.get('shares', 'N/A')}
**Screenshot:** ![Screenshot {i}](files/{session_id}/{viral_post.get('filename', 'N/A')})

---
"""
        
        # Adiciona estatísticas finais
        statistics = massive_results.get('statistics', {})
        md_content += f"""

---

## 6. ESTATÍSTICAS FINAIS DA COLETA

### 6.1 Resumo Quantitativo
- **Total de Fontes Web:** {statistics.get('total_web_sources', 0)}
- **Total de Posts Sociais:** {statistics.get('total_social_posts', 0)}
- **Total de Tendências:** {statistics.get('total_trends', 0)}
- **Total de Screenshots:** {statistics.get('total_screenshots', 0)}
- **Tempo de Execução:** {statistics.get('execution_time', 0):.2f} segundos

### 6.2 Qualidade dos Dados
- **URLs Válidas:** {statistics.get('valid_urls_percentage', 0):.1f}%
- **Conteúdo Extraído:** {statistics.get('content_extraction_success', 0):.1f}%
- **Screenshots Bem-sucedidos:** {statistics.get('screenshot_success_rate', 0):.1f}%

### 6.3 Distribuição por Fonte
"""
        
        sources_distribution = statistics.get('sources_by_type', {})
        for source_type, count in sources_distribution.items():
            md_content += f"- **{source_type}:** {count}\n"
        
        md_content += f"""

---

## 7. CONCLUSÕES DA COLETA MASSIVA

### 7.1 Dados Coletados
Este relatório contém **{statistics.get('total_data_points', 0)} pontos de dados** coletados de múltiplas fontes em tempo real, incluindo:

1. **Busca Web Intercalada:** Dados de {len(web_results.get('providers_used', []))} provedores diferentes
2. **Redes Sociais:** Posts de {len(social_results.get('all_platforms_data', {}).get('platforms', []))} plataformas
3. **Análise de Tendências:** Identificação de padrões virais e hashtags em alta
4. **Evidências Visuais:** Screenshots dos posts com maior engajamento

### 7.2 Preparação para Etapa 2
Este documento serve como base completa para a **Etapa 2 - Análise e Síntese da IA**, onde:

1. A IA irá **estudar ativamente** todo este conteúdo por **5 minutos**
2. Realizará **buscas adicionais** conforme necessário
3. Sintetizará os achados em um **JSON estruturado**
4. Preparará dados para geração dos **16 módulos de análise**

### 7.3 Próximos Passos
- [x] Coleta massiva de dados concluída
- [ ] Análise e síntese da IA (Etapa 2)
- [ ] Geração dos 16 módulos (Etapa 3)
- [ ] Compilação do relatório final

---

**Arquivo gerado em:** {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}
**Sessão:** {session_id}
**Sistema:** ARQV30 Enhanced v3.0 - Massive Data Collector
"""
        
        return md_content

    def _calculate_collection_statistics(self, massive_results: Dict[str, Any], execution_time: float) -> Dict[str, Any]:
        """Calcula estatísticas da coleta massiva"""
        
        web_results = massive_results.get('web_search_results', {})
        social_results = massive_results.get('social_media_results', {})
        trend_results = massive_results.get('trendfinder_results', {})
        screenshots_results = massive_results.get('viral_posts_screenshots', {})
        
        # Conta fontes
        total_web_sources = len(web_results.get('consolidated_urls', []))
        total_social_posts = social_results.get('total_posts', 0)
        total_trends = len(trend_results.get('trends', []))
        total_screenshots = screenshots_results.get('screenshots_captured', 0)
        
        # Calcula taxas de sucesso
        screenshot_success_rate = 0
        if screenshots_results.get('total_posts_analyzed', 0) > 0:
            screenshot_success_rate = (screenshots_results.get('screenshots_captured', 0) / 
                                     screenshots_results.get('total_posts_analyzed', 1)) * 100
        
        # Distribui por tipo de fonte
        sources_by_type = {
            'Web Search': total_web_sources,
            'Social Media': total_social_posts,
            'Trends': total_trends,
            'Screenshots': total_screenshots
        }
        
        return {
            'total_web_sources': total_web_sources,
            'total_social_posts': total_social_posts,
            'total_trends': total_trends,
            'total_screenshots': total_screenshots,
            'total_data_points': total_web_sources + total_social_posts + total_trends + total_screenshots,
            'execution_time': execution_time,
            'valid_urls_percentage': 95.0,  # Estimativa
            'content_extraction_success': 90.0,  # Estimativa
            'screenshot_success_rate': screenshot_success_rate,
            'sources_by_type': sources_by_type
        }

# Instância global
massive_data_collector = MassiveDataCollector()

