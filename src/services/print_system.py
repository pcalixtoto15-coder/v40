#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Print Corrigido - V40 Enhanced
Sistema robusto para captura de screenshots e prints de páginas web
"""

import os
import logging
import time
from typing import Dict, List, Any, Optional
from datetime import datetime
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
import base64
from PIL import Image
import io

logger = logging.getLogger(__name__)

class PrintSystem:
    """Sistema de captura de screenshots aprimorado"""
    
    def __init__(self):
        """Inicializa o sistema de print"""
        self.driver = None
        self.screenshots_dir = "/home/ubuntu/v40_enhanced/screenshots"
        self.ensure_screenshots_dir()
        logger.info("✅ Sistema de Print inicializado")
    
    def ensure_screenshots_dir(self):
        """Garante que o diretório de screenshots existe"""
        os.makedirs(self.screenshots_dir, exist_ok=True)
    
    def setup_driver(self):
        """Configura o driver do Chrome para screenshots"""
        try:
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            chrome_options.add_argument('--disable-extensions')
            chrome_options.add_argument('--disable-plugins')
            chrome_options.add_argument('--disable-images')
            chrome_options.add_argument('--disable-javascript')
            
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.set_page_load_timeout(30)
            logger.info("✅ Driver Chrome configurado com sucesso")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro ao configurar driver: {e}")
            return False
    
    def capture_screenshot(self, url: str, filename: str = None) -> Dict[str, Any]:
        """Captura screenshot de uma URL"""
        try:
            if not self.driver:
                if not self.setup_driver():
                    return {"success": False, "error": "Falha ao configurar driver"}
            
            # Gera nome do arquivo se não fornecido
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"screenshot_{timestamp}.png"
            
            filepath = os.path.join(self.screenshots_dir, filename)
            
            # Navega para a URL
            logger.info(f"📸 Capturando screenshot de: {url}")
            self.driver.get(url)
            
            # Aguarda carregamento
            time.sleep(3)
            
            # Captura screenshot
            screenshot_data = self.driver.get_screenshot_as_png()
            
            # Salva arquivo
            with open(filepath, 'wb') as f:
                f.write(screenshot_data)
            
            # Otimiza imagem
            self.optimize_image(filepath)
            
            logger.info(f"✅ Screenshot salvo: {filepath}")
            
            return {
                "success": True,
                "filepath": filepath,
                "filename": filename,
                "url": url,
                "timestamp": datetime.now().isoformat(),
                "size": os.path.getsize(filepath)
            }
            
        except Exception as e:
            logger.error(f"❌ Erro ao capturar screenshot: {e}")
            return {
                "success": False,
                "error": str(e),
                "url": url
            }
    
    def capture_multiple_screenshots(self, urls: List[str]) -> List[Dict[str, Any]]:
        """Captura screenshots de múltiplas URLs"""
        results = []
        
        for i, url in enumerate(urls):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{i+1}_{timestamp}.png"
            
            result = self.capture_screenshot(url, filename)
            results.append(result)
            
            # Pequena pausa entre capturas
            time.sleep(2)
        
        return results
    
    def capture_social_media_post(self, platform: str, post_url: str) -> Dict[str, Any]:
        """Captura screenshot específico para posts de redes sociais"""
        try:
            if not self.driver:
                if not self.setup_driver():
                    return {"success": False, "error": "Falha ao configurar driver"}
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{platform}_post_{timestamp}.png"
            filepath = os.path.join(self.screenshots_dir, filename)
            
            logger.info(f"📱 Capturando post do {platform}: {post_url}")
            
            # Configurações específicas por plataforma
            if platform.lower() == 'instagram':
                self.driver.set_window_size(414, 896)  # Mobile size
            elif platform.lower() == 'twitter':
                self.driver.set_window_size(1200, 800)
            elif platform.lower() == 'linkedin':
                self.driver.set_window_size(1200, 900)
            else:
                self.driver.set_window_size(1920, 1080)
            
            # Navega para o post
            self.driver.get(post_url)
            
            # Aguarda carregamento específico da plataforma
            wait_time = 5 if platform.lower() in ['instagram', 'twitter'] else 3
            time.sleep(wait_time)
            
            # Tenta encontrar o elemento do post
            try:
                if platform.lower() == 'instagram':
                    post_element = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.TAG_NAME, "article"))
                    )
                elif platform.lower() == 'twitter':
                    post_element = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='tweet']"))
                    )
                else:
                    post_element = self.driver.find_element(By.TAG_NAME, "body")
                
                # Captura screenshot do elemento específico
                screenshot_data = post_element.screenshot_as_png
                
            except (TimeoutException, WebDriverException):
                # Fallback para screenshot da página inteira
                screenshot_data = self.driver.get_screenshot_as_png()
            
            # Salva arquivo
            with open(filepath, 'wb') as f:
                f.write(screenshot_data)
            
            # Otimiza imagem
            self.optimize_image(filepath)
            
            logger.info(f"✅ Screenshot do {platform} salvo: {filepath}")
            
            return {
                "success": True,
                "filepath": filepath,
                "filename": filename,
                "platform": platform,
                "post_url": post_url,
                "timestamp": datetime.now().isoformat(),
                "size": os.path.getsize(filepath)
            }
            
        except Exception as e:
            logger.error(f"❌ Erro ao capturar post do {platform}: {e}")
            return {
                "success": False,
                "error": str(e),
                "platform": platform,
                "post_url": post_url
            }
    
    def optimize_image(self, filepath: str):
        """Otimiza a imagem para reduzir tamanho"""
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
                
                # Salva com qualidade otimizada
                img.save(filepath, 'PNG', optimize=True, quality=85)
                
        except Exception as e:
            logger.warning(f"⚠️ Erro ao otimizar imagem {filepath}: {e}")
    
    def get_screenshot_info(self, filename: str) -> Dict[str, Any]:
        """Obtém informações sobre um screenshot"""
        filepath = os.path.join(self.screenshots_dir, filename)
        
        if not os.path.exists(filepath):
            return {"success": False, "error": "Arquivo não encontrado"}
        
        try:
            with Image.open(filepath) as img:
                return {
                    "success": True,
                    "filename": filename,
                    "filepath": filepath,
                    "size": os.path.getsize(filepath),
                    "dimensions": img.size,
                    "format": img.format,
                    "mode": img.mode,
                    "created": datetime.fromtimestamp(os.path.getctime(filepath)).isoformat()
                }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def list_screenshots(self) -> List[Dict[str, Any]]:
        """Lista todos os screenshots disponíveis"""
        screenshots = []
        
        try:
            for filename in os.listdir(self.screenshots_dir):
                if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                    info = self.get_screenshot_info(filename)
                    if info["success"]:
                        screenshots.append(info)
            
            # Ordena por data de criação (mais recente primeiro)
            screenshots.sort(key=lambda x: x["created"], reverse=True)
            
        except Exception as e:
            logger.error(f"❌ Erro ao listar screenshots: {e}")
        
        return screenshots
    
    def cleanup_old_screenshots(self, days: int = 7):
        """Remove screenshots antigos"""
        try:
            current_time = time.time()
            cutoff_time = current_time - (days * 24 * 60 * 60)
            
            removed_count = 0
            for filename in os.listdir(self.screenshots_dir):
                filepath = os.path.join(self.screenshots_dir, filename)
                if os.path.getctime(filepath) < cutoff_time:
                    os.remove(filepath)
                    removed_count += 1
            
            logger.info(f"🧹 Removidos {removed_count} screenshots antigos")
            return {"success": True, "removed_count": removed_count}
            
        except Exception as e:
            logger.error(f"❌ Erro na limpeza de screenshots: {e}")
            return {"success": False, "error": str(e)}
    
    def close(self):
        """Fecha o driver"""
        if self.driver:
            try:
                self.driver.quit()
                self.driver = None
                logger.info("✅ Driver fechado com sucesso")
            except Exception as e:
                logger.error(f"❌ Erro ao fechar driver: {e}")

# Instância global
print_system = PrintSystem()

def get_print_system():
    """Retorna a instância global do sistema de print"""
    return print_system

