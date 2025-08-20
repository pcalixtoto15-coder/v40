#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v3.0 - Visual Content Capture CORRIGIDO
Sistema de captura de screenshots de posts de redes sociais com maior conversão
"""

import os
import logging
import time
import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime
from pathlib import Path

# Selenium imports
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image

logger = logging.getLogger(__name__)

class VisualContentCapture:
    """Sistema de captura de screenshots CORRIGIDO para posts virais"""

    def __init__(self):
        """Inicializa o capturador visual"""
        self.driver = None
        self.wait_timeout = 15
        self.page_load_timeout = 45
        self.screenshots_base_dir = "analyses_data/files"
        
        logger.info("📸 Visual Content Capture CORRIGIDO inicializado")

    def _setup_driver(self) -> webdriver.Chrome:
        """Configura o driver do Chrome otimizado para captura"""
        try:
            chrome_options = Options()
            
            # Configurações otimizadas para captura de redes sociais
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--disable-plugins")
            # NÃO desabilitar imagens e JS para redes sociais
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
            
            # Instala automaticamente o ChromeDriver
            service = Service(ChromeDriverManager().install())
            
            driver = webdriver.Chrome(service=service, options=chrome_options)
            driver.set_page_load_timeout(self.page_load_timeout)
            
            logger.info("✅ Chrome driver configurado para captura de redes sociais")
            return driver
            
        except Exception as e:
            logger.error(f"❌ Erro ao configurar Chrome driver: {e}")
            raise

    def _create_session_directory(self, session_id: str) -> Path:
        """Cria diretório para a sessão"""
        try:
            session_dir = Path(self.screenshots_base_dir) / session_id
            session_dir.mkdir(parents=True, exist_ok=True)
            
            logger.info(f"📁 Diretório criado: {session_dir}")
            return session_dir
            
        except Exception as e:
            logger.error(f"❌ Erro ao criar diretório: {e}")
            raise

    def _optimize_screenshot(self, filepath: str):
        """Otimiza screenshot para melhor qualidade e tamanho"""
        try:
            with Image.open(filepath) as img:
                # Converte para RGB se necessário
                if img.mode in ('RGBA', 'LA', 'P'):
                    img = img.convert('RGB')
                
                # Redimensiona se muito grande
                max_width = 1920
                max_height = 1080
                
                if img.width > max_width or img.height > max_height:
                    img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
                
                # Salva otimizado
                img.save(filepath, 'PNG', optimize=True, quality=85)
                
        except Exception as e:
            logger.warning(f"⚠️ Erro ao otimizar screenshot {filepath}: {e}")

    def _capture_social_media_post(self, url: str, platform: str, session_dir: Path, index: int) -> Dict[str, Any]:
        """Captura screenshot específico para posts de redes sociais"""
        try:
            logger.info(f"📱 Capturando post {platform}: {url}")
            
            # Configurações específicas por plataforma
            if platform.lower() == 'instagram':
                self.driver.set_window_size(414, 896)  # Mobile size
            elif platform.lower() == 'twitter':
                self.driver.set_window_size(1200, 800)
            elif platform.lower() == 'linkedin':
                self.driver.set_window_size(1200, 900)
            elif platform.lower() == 'youtube':
                self.driver.set_window_size(1280, 720)
            else:
                self.driver.set_window_size(1920, 1080)
            
            # Acessa a URL
            self.driver.get(url)
            
            # Aguarda carregamento específico por plataforma
            wait_time = 8 if platform.lower() in ['instagram', 'twitter', 'youtube'] else 6
            time.sleep(wait_time)
            
            # Tenta capturar elemento específico do post
            screenshot_data = None
            try:
                if platform.lower() == 'instagram':
                    post_element = WebDriverWait(self.driver, self.wait_timeout).until(
                        EC.presence_of_element_located((By.TAG_NAME, "article"))
                    )
                    screenshot_data = post_element.screenshot_as_png
                elif platform.lower() == 'twitter':
                    post_element = WebDriverWait(self.driver, self.wait_timeout).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='tweet']"))
                    )
                    screenshot_data = post_element.screenshot_as_png
                elif platform.lower() == 'youtube':
                    post_element = WebDriverWait(self.driver, self.wait_timeout).until(
                        EC.presence_of_element_located((By.ID, "player-container"))
                    )
                    screenshot_data = post_element.screenshot_as_png
                else:
                    screenshot_data = self.driver.get_screenshot_as_png()
                
            except (TimeoutException, WebDriverException) as e:
                logger.warning(f"⚠️ Elemento específico não encontrado para {platform}. Capturando página inteira.")
                screenshot_data = self.driver.get_screenshot_as_png()
            
            # Salva screenshot
            filename = f"{platform}_post_{index:03d}.png"
            filepath = session_dir / filename
            
            with open(filepath, 'wb') as f:
                f.write(screenshot_data)
            
            # Otimiza imagem
            self._optimize_screenshot(str(filepath))
            
            # Captura informações da página
            page_title = self.driver.title or "Sem título"
            page_url = self.driver.current_url
            
            logger.info(f"✅ Screenshot {platform} salvo: {filepath}")
            
            return {
                'success': True,
                'url': url,
                'final_url': page_url,
                'title': page_title,
                'platform': platform,
                'filename': filename,
                'filepath': str(filepath),
                'filesize': filepath.stat().st_size,
                'timestamp': datetime.now().isoformat()
            }
                
        except Exception as e:
            error_msg = f"Erro ao capturar {platform} post de {url}: {e}"
            logger.error(f"❌ {error_msg}")
            
            return {
                'success': False,
                'url': url,
                'platform': platform,
                'error': error_msg,
                'timestamp': datetime.now().isoformat()
            }

    async def capture_viral_posts_screenshots(self, social_media_data: Dict[str, Any], session_id: str) -> Dict[str, Any]:
        """
        Captura screenshots dos posts com maior conversão/engajamento
        
        Args:
            social_media_data: Dados das redes sociais com posts ranqueados
            session_id: ID da sessão para organização
        """
        logger.info(f"📸 Iniciando captura de posts virais para sessão {session_id}")
        
        # Resultado da operação
        capture_results = {
            'session_id': session_id,
            'total_posts_analyzed': 0,
            'screenshots_captured': 0,
            'failed_captures': 0,
            'viral_posts': [],
            'errors': [],
            'start_time': datetime.now().isoformat(),
            'session_directory': None
        }
        
        try:
            # Cria diretório da sessão
            session_dir = self._create_session_directory(session_id)
            capture_results['session_directory'] = str(session_dir)
            
            # Configura o driver
            self.driver = self._setup_driver()
            
            # Identifica posts com maior engajamento de cada plataforma
            viral_posts = self._identify_viral_posts(social_media_data)
            capture_results['total_posts_analyzed'] = len(viral_posts)
            
            # Captura screenshots dos posts virais
            for i, post_data in enumerate(viral_posts, 1):
                try:
                    url = post_data.get('url')
                    platform = post_data.get('platform', 'unknown')
                    
                    if not url or not url.startswith(('http://', 'https://')):
                        logger.warning(f"⚠️ URL inválida ignorada: {url}")
                        capture_results['failed_captures'] += 1
                        capture_results['errors'].append(f"URL inválida: {url}")
                        continue
                    
                    # Captura o screenshot
                    result = self._capture_social_media_post(url, platform, session_dir, i)
                    
                    if result['success']:
                        result.update({
                            'engagement_score': post_data.get('engagement_score', 0),
                            'views': post_data.get('views', 0),
                            'likes': post_data.get('likes', 0),
                            'shares': post_data.get('shares', 0)
                        })
                        capture_results['screenshots_captured'] += 1
                        capture_results['viral_posts'].append(result)
                    else:
                        capture_results['failed_captures'] += 1
                        capture_results['errors'].append(result['error'])
                    
                    # Pausa entre capturas
                    await asyncio.sleep(2)
                    
                except Exception as e:
                    error_msg = f"Erro processando post viral {i}: {e}"
                    logger.error(f"❌ {error_msg}")
                    capture_results['failed_captures'] += 1
                    capture_results['errors'].append(error_msg)
            
            # Finaliza a captura
            capture_results['end_time'] = datetime.now().isoformat()
            
            logger.info(f"✅ Captura de posts virais concluída: {capture_results['screenshots_captured']}/{capture_results['total_posts_analyzed']} sucessos")
            
        except Exception as e:
            error_msg = f"Erro crítico na captura de posts virais: {e}"
            logger.error(f"❌ {error_msg}")
            capture_results['critical_error'] = error_msg
            
        finally:
            # Fecha o driver se estiver aberto
            if self.driver:
                try:
                    self.driver.quit()
                    logger.info("✅ Chrome driver fechado")
                except Exception as e:
                    logger.error(f"❌ Erro ao fechar driver: {e}")
                self.driver = None
        
        return capture_results

    def _identify_viral_posts(self, social_media_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identifica os posts com maior engajamento/conversão"""
        viral_posts = []
        
        try:
            # Processa cada plataforma
            for platform_name in ['youtube', 'twitter', 'instagram', 'linkedin']:
                platform_data = social_media_data.get(platform_name, {})
                posts = platform_data.get('results', [])
                
                if not posts:
                    continue
                
                # Calcula score de engajamento para cada post
                scored_posts = []
                for post in posts:
                    engagement_score = self._calculate_engagement_score(post, platform_name)
                    if engagement_score > 0:
                        post_data = {
                            'url': post.get('url', ''),
                            'platform': platform_name,
                            'engagement_score': engagement_score,
                            'title': post.get('title', post.get('text', post.get('caption', ''))),
                            'views': post.get('view_count', post.get('like_count', 0)),
                            'likes': post.get('like_count', 0),
                            'shares': post.get('retweet_count', post.get('shares', 0))
                        }
                        scored_posts.append(post_data)
                
                # Ordena por engajamento e pega os top 3 de cada plataforma
                scored_posts.sort(key=lambda x: x['engagement_score'], reverse=True)
                viral_posts.extend(scored_posts[:3])
            
            # Ordena todos os posts por engajamento e pega os top 10 globais
            viral_posts.sort(key=lambda x: x['engagement_score'], reverse=True)
            viral_posts = viral_posts[:10]
            
            logger.info(f"🎯 Identificados {len(viral_posts)} posts virais para captura")
            
        except Exception as e:
            logger.error(f"❌ Erro ao identificar posts virais: {e}")
        
        return viral_posts

    def _calculate_engagement_score(self, post: Dict[str, Any], platform: str) -> float:
        """Calcula score de engajamento baseado na plataforma"""
        try:
            if platform == 'youtube':
                views = int(str(post.get('view_count', 0)).replace(',', ''))
                likes = post.get('like_count', 0)
                comments = post.get('comment_count', 0)
                return (likes * 2 + comments * 3) / max(views, 1) * 1000
                
            elif platform == 'twitter':
                likes = post.get('like_count', 0)
                retweets = post.get('retweet_count', 0)
                replies = post.get('reply_count', 0)
                return likes + (retweets * 3) + (replies * 2)
                
            elif platform == 'instagram':
                likes = post.get('like_count', 0)
                comments = post.get('comment_count', 0)
                return likes + (comments * 5)
                
            elif platform == 'linkedin':
                likes = post.get('likes', 0)
                comments = post.get('comments', 0)
                shares = post.get('shares', 0)
                return likes + (comments * 3) + (shares * 5)
                
        except Exception as e:
            logger.warning(f"⚠️ Erro ao calcular engajamento: {e}")
        
        return 0

    def cleanup_old_screenshots(self, days_old: int = 7):
        """Remove screenshots antigos para economizar espaço"""
        try:
            files_dir = Path(self.screenshots_base_dir)
            if not files_dir.exists():
                return
            
            cutoff_time = time.time() - (days_old * 24 * 60 * 60)
            removed_count = 0
            
            for session_dir in files_dir.iterdir():
                if session_dir.is_dir():
                    for screenshot in session_dir.glob("*.png"):
                        if screenshot.stat().st_mtime < cutoff_time:
                            screenshot.unlink()
                            removed_count += 1
                    
                    # Remove diretório se estiver vazio
                    try:
                        session_dir.rmdir()
                    except OSError:
                        pass  # Diretório não está vazio
            
            if removed_count > 0:
                logger.info(f"🧹 Removidos {removed_count} screenshots antigos")
                
        except Exception as e:
            logger.error(f"❌ Erro na limpeza: {e}")

# Instância global
visual_content_capture = VisualContentCapture()

