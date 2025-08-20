#!/usr/bin/env python3
import os
import time
import logging
from typing import Dict, Any
from datetime import datetime

# Importa o sistema de IA aprimorado
try:
    from .enhanced_ai_manager import EnhancedAIManager
    HAS_ENHANCED_AI = True
except ImportError:
    HAS_ENHANCED_AI = False

# Fallback para Gemini direto se não tiver o sistema aprimorado
try:
    import google.generativeai as genai
    HAS_GEMINI = True
except ImportError:
    HAS_GEMINI = False

logger = logging.getLogger(__name__)

class GeminiReportGenerator:
    def __init__(self):
        """Inicializa o gerador de relatórios com IA aprimorada"""
        self.ai_manager = None
        
        # Tenta usar o sistema de IA aprimorado primeiro
        if HAS_ENHANCED_AI:
            try:
                self.ai_manager = EnhancedAIManager()
                logger.info("✅ Sistema de IA aprimorado inicializado (Qwen/OpenRouter + Gemini)")
            except Exception as e:
                logger.error(f"❌ Erro ao inicializar sistema de IA aprimorado: {e}")
                self.ai_manager = None
        
        # Fallback para Gemini direto
        if not self.ai_manager and HAS_GEMINI:
            try:
                genai.configure(api_key=os.getenv('GEMINI_API_KEY', 'demo-key'))
                self.model = genai.GenerativeModel("gemini-pro")
                logger.info("✅ Gemini direto configurado como fallback")
            except Exception as e:
                logger.error(f"❌ Erro ao configurar Gemini: {e}")
                self.model = None
        else:
            self.model = None

    def study_and_generate_report(self, markdown_content: str, study_time_minutes: int = 5) -> str:
        """Simula o 'estudo' da IA sobre o conteúdo do markdown e gera um relatório."""
        logger.info(f"🧠 Iniciando 'estudo' da IA sobre o conteúdo do markdown por {study_time_minutes} minutos...")
        
        # Simula o tempo de processamento/estudo
        time.sleep(study_time_minutes * 60) 
        
        logger.info("✅ 'Estudo' da IA concluído. Gerando relatório...")
        
        prompt = f"""
        Você é um especialista em análise de mercado. Estude o seguinte documento detalhado em Markdown e gere um relatório robusto e conciso, destacando os principais insights, tendências e recomendações. Inclua um resumo executivo, análise de mercado (Alibaba), análise de mídias sociais e conclusões.

        Documento para estudo:
        {markdown_content}

        Estrutura do relatório:
        # Relatório de Análise de Mercado
        ## Resumo Executivo
        ## Análise Alibaba (Principais Produtos e Fornecedores)
        ## Análise de Mídias Sociais (Sentimento e Engajamento)
        ## Conclusões e Recomendações
        """
        
        try:
            # Usa o sistema de IA aprimorado se disponível
            if self.ai_manager:
                # Usa geração com busca ativa para relatórios mais robustos
                import asyncio
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    response = loop.run_until_complete(
                        self.ai_manager.generate_with_active_search(
                            prompt=prompt,
                            context=markdown_content[:2000],  # Limita contexto para evitar overflow
                            session_id="report_generation",
                            max_search_iterations=2
                        )
                    )
                    return response
                finally:
                    loop.close()
            
            # Fallback para Gemini direto
            elif self.model:
                response = self.model.generate_content(prompt)
                return response.text
            
            else:
                raise Exception("Nenhum sistema de IA disponível")
                
        except Exception as e:
            logger.error(f"❌ Erro ao gerar relatório com IA: {e}")
            return self._generate_fallback_report_from_markdown(markdown_content)

    def _generate_fallback_report_from_markdown(self, markdown_content: str) -> str:
        """Relatório de fallback simplificado a partir do markdown."""
        return f"""# Relatório de Análise de Mercado (Fallback)
## Resumo Executivo
Este é um relatório de fallback gerado em {datetime.now().strftime("%d/%m/%Y %H:%M")}.

Devido a um erro na geração completa, apresentamos um resumo simplificado do conteúdo estudado.

## Conteúdo Principal do Documento:

{markdown_content[:1000]}... (conteúdo truncado para brevidade)

## Conclusões
Por favor, revise o log para mais detalhes sobre o erro na geração do relatório completo.
"""

    def generate_comprehensive_report(self, data: Dict[str, Any]) -> str:
        """Método original, agora adaptado para usar o estudo ou ser um fallback."""
        # Este método pode ser adaptado para chamar study_and_generate_report
        # ou ser um ponto de entrada para relatórios mais simples sem 'estudo' prolongado.
        # Por simplicidade, vamos usá-lo como um wrapper para o estudo agora.
        
        # Converte os dados em um formato markdown para o 'estudo'
        temp_markdown_content = f"""
# Dados da Análise

## Dados Alibaba
{data.get("alibaba_data", {})}

## Dados Social Media
{data.get("social_data", {})}

## Screenshots Capturados
{data.get("screenshots", [])}
"""
        return self.study_and_generate_report(temp_markdown_content, study_time_minutes=5)

gemini_reports = GeminiReportGenerator()

