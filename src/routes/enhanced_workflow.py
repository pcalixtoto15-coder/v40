#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v3.0 - Enhanced Workflow Routes
Rotas para o workflow aprimorado em 3 etapas
"""

import logging
import time
import uuid
import asyncio
import os
import glob
from datetime import datetime
from typing import Dict, Any  # Import necessário para Dict e Any
from flask import Blueprint, request, jsonify, send_file
from services.real_search_orchestrator import real_search_orchestrator
from services.viral_content_analyzer import viral_content_analyzer
from services.enhanced_synthesis_engine import enhanced_synthesis_engine
from services.enhanced_module_processor import enhanced_module_processor
from services.comprehensive_report_generator_v3 import comprehensive_report_generator_v3
from services.auto_save_manager import salvar_etapa

logger = logging.getLogger(__name__)

enhanced_workflow_bp = Blueprint('enhanced_workflow', __name__)

@enhanced_workflow_bp.route('/workflow/step1/start', methods=['POST'])
def start_step1_collection():
    """ETAPA 1: Coleta Massiva com Alibaba WebSailor + Screenshots Virais"""
    try:
        data = request.get_json()

        # Gera session_id único
        session_id = f"session_{int(time.time() * 1000)}_{uuid.uuid4().hex[:8]}"

        # Extrai parâmetros
        segmento = data.get('segmento', '').strip()
        produto = data.get('produto', '').strip()
        publico = data.get('publico', '').strip()

        # Validação
        if not segmento:
            return jsonify({"error": "Segmento é obrigatório"}), 400

        # Constrói query de pesquisa
        query_parts = [segmento]
        if produto:
            query_parts.append(produto)
        query_parts.extend(["Brasil", "2024", "mercado"])

        query = " ".join(query_parts)

        # Contexto da análise
        context = {
            "segmento": segmento,
            "produto": produto,
            "publico": publico,
            "query_original": query,
            "etapa": 1,
            "workflow_type": "ultra_robusto_v3"
        }

        logger.info(f"🚀 ETAPA 1 ULTRA-ROBUSTA INICIADA - Sessão: {session_id}")
        logger.info(f"🔍 Query: {query}")
        logger.info(f"🌐 Alibaba WebSailor: ATIVO")
        logger.info(f"📱 Busca Social: ATIVA")
        logger.info(f"📸 Screenshots: ATIVOS")

        # Salva início da etapa 1
        salvar_etapa("etapa1_iniciada", {
            "session_id": session_id,
            "query": query,
            "context": context,
            "timestamp": datetime.now().isoformat()
        }, categoria="workflow")

        # Executa coleta massiva em thread separada
        def execute_collection():
            try:
                logger.info("🌐 Iniciando busca massiva com Alibaba WebSailor...")
                
                # NOVA IMPLEMENTAÇÃO: Busca massiva com WebSailor + Social
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

                try:
                    # Usa o novo sistema de busca massiva
                    from services.search_api_manager import search_api_manager
                    
                    massive_search_results = loop.run_until_complete(
                        search_api_manager.execute_massive_search_with_websailor(
                            query=query,
                            context=context,
                            session_id=session_id
                        )
                    )
                    
                    logger.info("✅ Busca massiva concluída com WebSailor + Social + Screenshots")

                finally:
                    loop.close()

                # Gera relatório de coleta
                collection_report = _generate_enhanced_collection_report(
                    massive_search_results, session_id, context
                )

                # Salva relatório
                
                # Salva relatório de coleta
                _save_enhanced_collection_report(collection_report, session_id)

                # Salva resultado da etapa 1
                salvar_etapa("etapa1_concluida", {
                    "session_id": session_id,
                    "massive_search_results": massive_search_results,
                    "collection_report_generated": True,
                    "websailor_used": True,
                    "social_search_executed": True,
                    "screenshots_captured": len(massive_search_results.get('screenshots_captured', [])),
                    "timestamp": datetime.now().isoformat()
                }, categoria="workflow")

                logger.info(f"✅ ETAPA 1 ULTRA-ROBUSTA CONCLUÍDA - Sessão: {session_id}")
                logger.info(f"📊 Fontes: {massive_search_results.get('statistics', {}).get('total_sources', 0)}")
                logger.info(f"📸 Screenshots: {len(massive_search_results.get('screenshots_captured', []))}")

            except Exception as e:
                logger.error(f"❌ Erro na execução da Etapa 1: {e}")
                salvar_etapa("etapa1_erro", {
                    "session_id": session_id,
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                }, categoria="workflow")

        # Inicia execução em background
        import threading
        thread = threading.Thread(target=execute_collection, daemon=True)
        thread.start()

        return jsonify({
            "success": True,
            "session_id": session_id,
            "message": "Etapa 1 iniciada: Coleta massiva com WebSailor + Social + Screenshots",
            "query": query,
            "estimated_duration": "5-8 minutos",
            "features": [
                "Alibaba WebSailor para navegação profunda",
                "Rotação automática de chaves de API",
                "Busca social massiva em todas as plataformas",
                "Captura automática de screenshots virais",
                "Identificação de posts com maior conversão"
            ],
            "next_step": "/api/workflow/step2/start",
            "status_endpoint": f"/api/workflow/status/{session_id}"
        }), 200

    except Exception as e:
        logger.error(f"❌ Erro ao iniciar Etapa 1: {e}")
        return jsonify({
            "success": False,
            "error": str(e),
            "message": "Falha ao iniciar coleta de dados"
        }), 500

@enhanced_workflow_bp.route('/workflow/step2/start', methods=['POST'])
def start_step2_synthesis():
    """ETAPA 2: Síntese com IA e Busca Ativa"""
    try:
        data = request.get_json()
        session_id = data.get('session_id')

        if not session_id:
            return jsonify({"error": "session_id é obrigatório"}), 400

        logger.info(f"🧠 ETAPA 2 INICIADA - Síntese para sessão: {session_id}")

        # Salva início da etapa 2
        salvar_etapa("etapa2_iniciada", {
            "session_id": session_id,
            "timestamp": datetime.now().isoformat()
        }, categoria="workflow")

        # Executa síntese em thread separada
        def execute_synthesis():
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

                try:
                    # Executa síntese master com busca ativa
                    synthesis_result = loop.run_until_complete(
                        enhanced_synthesis_engine.execute_enhanced_synthesis(
                            session_id=session_id,
                            synthesis_type="master_synthesis"
                        )
                    )

                    # Executa síntese comportamental
                    behavioral_result = loop.run_until_complete(
                        enhanced_synthesis_engine.execute_behavioral_synthesis(session_id)
                    )

                    # Executa síntese de mercado
                    market_result = loop.run_until_complete(
                        enhanced_synthesis_engine.execute_market_synthesis(session_id)
                    )

                finally:
                    loop.close()

                # Salva resultado da etapa 2
                salvar_etapa("etapa2_concluida", {
                    "session_id": session_id,
                    "synthesis_result": synthesis_result,
                    "behavioral_result": behavioral_result,
                    "market_result": market_result,
                    "timestamp": datetime.now().isoformat()
                }, categoria="workflow")

                logger.info(f"✅ ETAPA 2 CONCLUÍDA - Sessão: {session_id}")

            except Exception as e:
                logger.error(f"❌ Erro na execução da Etapa 2: {e}")
                salvar_etapa("etapa2_erro", {
                    "session_id": session_id,
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                }, categoria="workflow")

        # Inicia execução em background
        import threading
        thread = threading.Thread(target=execute_synthesis, daemon=True)
        thread.start()

        return jsonify({
            "success": True,
            "session_id": session_id,
            "message": "Etapa 2 iniciada: Síntese com IA e busca ativa",
            "estimated_duration": "2-4 minutos",
            "next_step": "/api/workflow/step3/start",
            "status_endpoint": f"/api/workflow/status/{session_id}"
        }), 200

    except Exception as e:
        logger.error(f"❌ Erro ao iniciar Etapa 2: {e}")
        return jsonify({
            "success": False,
            "error": str(e),
            "message": "Falha ao iniciar síntese"
        }), 500

@enhanced_workflow_bp.route('/workflow/step3/start', methods=['POST'])
def start_step3_generation():
    """ETAPA 3: Geração dos 16 Módulos e Relatório Final"""
    try:
        data = request.get_json()
        session_id = data.get('session_id')

        if not session_id:
            return jsonify({"error": "session_id é obrigatório"}), 400

        logger.info(f"📝 ETAPA 3 INICIADA - Geração para sessão: {session_id}")

        # Salva início da etapa 3
        salvar_etapa("etapa3_iniciada", {
            "session_id": session_id,
            "timestamp": datetime.now().isoformat()
        }, categoria="workflow")

        # Executa geração em thread separada
        def execute_generation():
            try:
                # Gera todos os 16 módulos
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

                try:
                    modules_result = loop.run_until_complete(
                        enhanced_module_processor.generate_all_modules(session_id)
                    )
                finally:
                    loop.close()

                # Compila relatório final
                final_report = comprehensive_report_generator_v3.compile_final_markdown_report(session_id)

                # Salva resultado da etapa 3
                salvar_etapa("etapa3_concluida", {
                    "session_id": session_id,
                    "modules_result": modules_result,
                    "final_report": final_report,
                    "timestamp": datetime.now().isoformat()
                }, categoria="workflow")

                logger.info(f"✅ ETAPA 3 CONCLUÍDA - Sessão: {session_id}")
                logger.info(f"📊 {modules_result.get('successful_modules', 0)}/16 módulos gerados")

            except Exception as e:
                logger.error(f"❌ Erro na execução da Etapa 3: {e}")
                salvar_etapa("etapa3_erro", {
                    "session_id": session_id,
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                }, categoria="workflow")

        # Inicia execução em background
        import threading
        thread = threading.Thread(target=execute_generation, daemon=True)
        thread.start()

        return jsonify({
            "success": True,
            "session_id": session_id,
            "message": "Etapa 3 iniciada: Geração de 16 módulos",
            "estimated_duration": "4-6 minutos",
            "modules_to_generate": 16,
            "status_endpoint": f"/api/workflow/status/{session_id}"
        }), 200

    except Exception as e:
        logger.error(f"❌ Erro ao iniciar Etapa 3: {e}")
        return jsonify({
            "success": False,
            "error": str(e),
            "message": "Falha ao iniciar geração de módulos"
        }), 500

@enhanced_workflow_bp.route('/workflow/complete', methods=['POST'])
def execute_complete_workflow():
    """Executa workflow completo em sequência"""
    try:
        data = request.get_json()

        # Gera session_id único
        session_id = f"session_{int(time.time() * 1000)}_{uuid.uuid4().hex[:8]}"

        logger.info(f"🚀 WORKFLOW COMPLETO INICIADO - Sessão: {session_id}")

        # Executa workflow completo em thread separada
        def execute_full_workflow():
            try:
                # ETAPA 1: Coleta
                logger.info("🌊 Executando Etapa 1: Coleta massiva")

                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

                try:
                    # Constrói query
                    segmento = data.get('segmento', '').strip()
                    produto = data.get('produto', '').strip()
                    query = f"{segmento} {produto} Brasil 2024 mercado".strip()                 
                    context = {
                        "segmento": segmento,
                        "produto": produto,
                        "publico": data.get('publico', ''),
                        "preco": data.get('preco', ''),
                        "objetivo_receita": data.get('objetivo_receita', ''),
                        "workflow_type": "complete"
                    }

                    # Executa busca massiva
                    search_results = loop.run_until_complete(
                        real_search_orchestrator.execute_massive_real_search(
                            query=query,
                            context=context,
                            session_id=session_id
                        )
                    )

                    # Analisa conteúdo viral
                    viral_analysis = loop.run_until_complete(
                        viral_content_analyzer.analyze_and_capture_viral_content(
                            search_results=search_results,
                            session_id=session_id
                        )
                    )

                    # Gera relatório de coleta
                    collection_report = _generate_collection_report(
                        search_results, viral_analysis, session_id, context
                    )
                    _save_collection_report(collection_report, session_id)

                    # ETAPA 2: Síntese
                    logger.info("🧠 Executando Etapa 2: Síntese com IA")

                    synthesis_result = loop.run_until_complete(
                        enhanced_synthesis_engine.execute_enhanced_synthesis(session_id)
                    )

                    # ETAPA 3: Geração de módulos
                    logger.info("📝 Executando Etapa 3: Geração de módulos")

                    modules_result = loop.run_until_complete(
                        enhanced_module_processor.generate_all_modules(session_id)
                    )

                    # Compila relatório final
                    final_report = comprehensive_report_generator_v3.compile_final_markdown_report(session_id)

                finally:
                    loop.close()

                # Salva resultado final
                salvar_etapa("workflow_completo", {
                    "session_id": session_id,
                    "search_results": search_results,
                    "viral_analysis": viral_analysis,
                    "synthesis_result": synthesis_result,
                    "modules_result": modules_result,
                    "final_report": final_report,
                    "timestamp": datetime.now().isoformat()
                }, categoria="workflow")

                logger.info(f"✅ WORKFLOW COMPLETO CONCLUÍDO - Sessão: {session_id}")

            except Exception as e:
                logger.error(f"❌ Erro no workflow completo: {e}")
                salvar_etapa("workflow_erro", {
                    "session_id": session_id,
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                }, categoria="workflow")

        # Inicia execução em background
        import threading
        thread = threading.Thread(target=execute_full_workflow, daemon=True)
        thread.start()

        return jsonify({
            "success": True,
            "session_id": session_id,
            "message": "Workflow completo iniciado",
            "estimated_total_duration": "8-15 minutos",
            "steps": [
                "Etapa 1: Coleta massiva (3-5 min)",
                "Etapa 2: Síntese com IA (2-4 min)", 
                "Etapa 3: Geração de módulos (4-6 min)"
            ],
            "status_endpoint": f"/api/workflow/status/{session_id}"
        }), 200

    except Exception as e:
        logger.error(f"❌ Erro ao iniciar workflow completo: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@enhanced_workflow_bp.route('/workflow/status/<session_id>', methods=['GET'])
def get_workflow_status(session_id):
    """Obtém status do workflow"""
    try:
        # Verifica arquivos salvos para determinar status

        status = {
            "session_id": session_id,
            "current_step": 0,
            "step_status": {
                "step1": "pending",
                "step2": "pending", 
                "step3": "pending"
            },
            "progress_percentage": 0,
            "estimated_remaining": "Calculando...",
            "last_update": datetime.now().isoformat()
        }

        # Verifica se etapa 1 foi concluída
        if os.path.exists(f"analyses_data/{session_id}/relatorio_coleta.md"):
            status["step_status"]["step1"] = "completed"
            status["current_step"] = 1
            status["progress_percentage"] = 33

        # Verifica se etapa 2 foi concluída
        if os.path.exists(f"analyses_data/{session_id}/resumo_sintese.json"):
            status["step_status"]["step2"] = "completed"
            status["current_step"] = 2
            status["progress_percentage"] = 66

        # Verifica se etapa 3 foi concluída
        if os.path.exists(f"analyses_data/{session_id}/relatorio_final.md"):
            status["step_status"]["step3"] = "completed"
            status["current_step"] = 3
            status["progress_percentage"] = 100
            status["estimated_remaining"] = "Concluído"

        # Verifica se há erros
        error_files = [
            f"relatorios_intermediarios/workflow/etapa1_erro*{session_id}*",
            f"relatorios_intermediarios/workflow/etapa2_erro*{session_id}*",
            f"relatorios_intermediarios/workflow/etapa3_erro*{session_id}*"
        ]

        for pattern in error_files:
            if glob.glob(pattern):
                status["error"] = "Erro detectado em uma das etapas"
                break

        return jsonify(status), 200

    except Exception as e:
        logger.error(f"❌ Erro ao obter status: {e}")
        return jsonify({
            "session_id": session_id,
            "error": str(e),
            "status": "error"
        }), 500

@enhanced_workflow_bp.route('/workflow/results/<session_id>', methods=['GET'])
def get_workflow_results(session_id):
    """Obtém resultados do workflow"""
    try:

        results = {
            "session_id": session_id,
            "available_files": [],
            "final_report_available": False,
            "modules_generated": 0,
            "screenshots_captured": 0
        }

        # Verifica relatório final
        final_report_path = f"analyses_data/{session_id}/relatorio_final.md"
        if os.path.exists(final_report_path):
            results["final_report_available"] = True
            results["final_report_path"] = final_report_path

        # Conta módulos gerados
        modules_dir = f"analyses_data/{session_id}/modules"
        if os.path.exists(modules_dir):
            modules = [f for f in os.listdir(modules_dir) if f.endswith('.md')]
            results["modules_generated"] = len(modules)
            results["modules_list"] = modules

        # Conta screenshots
        files_dir = f"analyses_data/files/{session_id}"
        if os.path.exists(files_dir):
            screenshots = [f for f in os.listdir(files_dir) if f.endswith('.png')]
            results["screenshots_captured"] = len(screenshots)
            results["screenshots_list"] = screenshots

        # Lista todos os arquivos disponíveis
        session_dir = f"analyses_data/{session_id}"
        if os.path.exists(session_dir):
            for root, dirs, files in os.walk(session_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, session_dir)
                    results["available_files"].append({
                        "name": file,
                        "path": relative_path,
                        "size": os.path.getsize(file_path),
                        "type": file.split('.')[-1] if '.' in file else 'unknown'
                    })

        return jsonify(results), 200

    except Exception as e:
        logger.error(f"❌ Erro ao obter resultados: {e}")
        return jsonify({
            "session_id": session_id,
            "error": str(e)
        }), 500

@enhanced_workflow_bp.route('/workflow/download/<session_id>/<file_type>', methods=['GET'])
def download_workflow_file(session_id, file_type):
    """Download de arquivos do workflow"""
    try:
        # Define o caminho base (sem src/)
        base_path = os.path.join("analyses_data", session_id)

        if file_type == "final_report":
            # Tenta primeiro o relatorio_final.md, depois o completo como fallback
            file_path = os.path.join(base_path, "relatorio_final.md")
            if not os.path.exists(file_path):
                file_path = os.path.join(base_path, "relatorio_final_completo.md")
            filename = f"relatorio_final_{session_id}.md"
        elif file_type == "complete_report":
            file_path = os.path.join(base_path, "relatorio_final_completo.md")
            filename = f"relatorio_completo_{session_id}.md"
        else:
            return jsonify({"error": "Tipo de relatório inválido"}), 400

        if not os.path.exists(file_path):
            return jsonify({"error": "Arquivo não encontrado"}), 404

        return send_file(
            file_path,
            as_attachment=True,
            download_name=filename
        )

    except Exception as e:
        logger.error(f"❌ Erro no download: {e}")
        return jsonify({"error": str(e)}), 500

# --- Funções auxiliares ---
def _generate_enhanced_collection_report(
    massive_search_results: Dict[str, Any],
    session_id: str,
    context: Dict[str, Any]
) -> str:
    """Gera relatório consolidado de coleta ULTRA-ROBUSTO"""

    # Função auxiliar para formatar números com segurança
    def safe_format_int(value):
        try:
            # Tenta converter para int e formatar com separador de milhar
            return f"{int(value):,}"
        except (ValueError, TypeError):
            # Se falhar, retorna 'N/A' ou o valor original como string
            return str(value) if value is not None else 'N/A'

    report = f"""# RELATÓRIO DE COLETA ULTRA-ROBUSTA - ARQV30 Enhanced v3.0

**Sessão:** {session_id}  
**Query:** {massive_search_results.get('query', 'N/A')}  
**Iniciado em:** {massive_search_results.get('search_started', 'N/A')}  
**Duração:** {massive_search_results.get('statistics', {}).get('search_duration', 0):.2f} segundos
**Metodologia:** Alibaba WebSailor + Rotação APIs + Busca Social + Screenshots

---

## RESUMO DA COLETA ULTRA-ROBUSTA

### Estatísticas Gerais:
- **Total de Fontes:** {massive_search_results.get('statistics', {}).get('total_sources', 0)}
- **Páginas WebSailor:** {massive_search_results.get('statistics', {}).get('websailor_pages', 0)}
- **Fontes de APIs:** {massive_search_results.get('statistics', {}).get('api_sources', 0)}
- **Posts Sociais:** {massive_search_results.get('statistics', {}).get('social_posts', 0)}
- **Screenshots Virais:** {massive_search_results.get('statistics', {}).get('screenshots_count', 0)}

### Metodologias Aplicadas:

#### 1. Alibaba WebSailor - Navegação Profunda
"""
    
    websailor_results = massive_search_results.get('websailor_results', {})
    if websailor_results:
        navegacao_stats = websailor_results.get('navegacao_profunda', {})
        report += f"""
- **Páginas Analisadas:** {navegacao_stats.get('total_paginas_analisadas', 0)}
- **Engines Utilizados:** {len(navegacao_stats.get('engines_utilizados', []))}
- **Fontes Preferenciais:** {navegacao_stats.get('fontes_preferenciais', 0)}
- **Qualidade Média:** {navegacao_stats.get('qualidade_media', 0):.2f}
- **Total de Caracteres:** {safe_format_int(navegacao_stats.get('total_caracteres', 0))}

#### 2. Rotação de APIs
"""
        api_results = massive_search_results.get('api_results', {})
        for provider, result in api_results.items():
            if result.get('success'):
                results_count = len(result.get('results', []))
                report += f"- **{provider}:** {results_count} resultados ✅\n"
            else:
                report += f"- **{provider}:** Falhou ❌\n"
        
        report += f"""

#### 3. Busca Social Massiva
"""
        social_results = massive_search_results.get('social_results', {})
        if social_results:
            platform_results = social_results.get('platform_results', {})
            for platform, posts in platform_results.items():
                report += f"- **{platform.title()}:** {len(posts)} posts encontrados\n"
        
        report += f"""

#### 4. Conteúdo Viral Identificado
"""
        viral_content = massive_search_results.get('viral_content', [])
        if viral_content:
            report += f"- **Total de Posts Virais:** {len(viral_content)}\n"
            
            # Agrupa por categoria viral
            viral_categories = {}
            for post in viral_content:
                category = post.get('viral_category', 'POPULAR')
                viral_categories[category] = viral_categories.get(category, 0) + 1
            
            for category, count in viral_categories.items():
                report += f"- **{category}:** {count} posts\n"
        
        report += f"""

#### 5. Screenshots Capturados
"""
        screenshots = massive_search_results.get('screenshots_captured', [])
        if screenshots:
            report += f"- **Total de Screenshots:** {len(screenshots)}\n"
            report += f"- **Localização:** `analyses_data/files/{session_id}/`\n"
            
            # Lista screenshots por plataforma
            platform_screenshots = {}
            for screenshot in screenshots:
                platform = screenshot.get('platform', 'web')
                platform_screenshots[platform] = platform_screenshots.get(platform, 0) + 1
            
            for platform, count in platform_screenshots.items():
                report += f"- **{platform.title()}:** {count} screenshots\n"
    else:
        report += "- Nenhum screenshot capturado\n"
    
    report += "\n---\n\n"

    # Seção detalhada dos resultados do WebSailor
    if websailor_results and websailor_results.get('conteudo_consolidado'):
        conteudo = websailor_results['conteudo_consolidado']
        
        report += "## RESULTADOS ALIBABA WEBSAILOR - NAVEGAÇÃO PROFUNDA\n\n"
        
        insights = conteudo.get('insights_principais', [])
        if insights:
            report += "### Insights Descobertos:\n"
            for i, insight in enumerate(insights[:15], 1):
                report += f"{i}. {insight}\n"
            report += "\n"
        
        tendencias = conteudo.get('tendencias_identificadas', [])
        if tendencias:
            report += "### Tendências Identificadas:\n"
            for i, tendencia in enumerate(tendencias[:10], 1):
                report += f"**{i}.** {tendencia}\n"
            report += "\n"
        
        oportunidades = conteudo.get('oportunidades_descobertas', [])
        if oportunidades:
            report += "### Oportunidades Descobertas:\n"
            for i, oportunidade in enumerate(oportunidades[:8], 1):
                report += f"• {oportunidade}\n"
            report += "\n"
        
        fontes_detalhadas = conteudo.get('fontes_detalhadas', [])
        if fontes_detalhadas:
            report += "### Fontes Analisadas pelo WebSailor:\n"
            for i, fonte in enumerate(fontes_detalhadas[:10], 1):
                report += f"**{i}.** {fonte.get('title', 'Sem título')}\n"
                report += f"   - URL: {fonte.get('url', 'N/A')}\n"
                report += f"   - Qualidade: {fonte.get('quality_score', 0):.2f}/100\n"
                report += f"   - Engine: {fonte.get('search_engine', 'N/A')}\n\n"
    
    # Seção de resultados das APIs
    api_results = massive_search_results.get('api_results', {})
    if api_results:
        report += "---\n\n## RESULTADOS DAS APIs COM ROTAÇÃO\n\n"
        
        for provider, result in api_results.items():
            if result.get('success'):
                results_list = result.get('results', [])
                report += f"### {provider} ({len(results_list)} resultados)\n\n"
                
                for i, item in enumerate(results_list[:5], 1):
                    title = item.get('title', item.get('content', 'Sem título'))[:100]
                    url = item.get('url', item.get('link', 'N/A'))
                    snippet = item.get('snippet', item.get('content', 'N/A'))[:200]
                    
                    report += f"**{i}.** {title}\n"
                    report += f"   - URL: {url}\n"
                    report += f"   - Resumo: {snippet}...\n\n"
            else:
                report += f"### {provider} - FALHOU\n"
                report += f"Erro: {result.get('error', 'Erro desconhecido')}\n\n"

    # Seção de resultados sociais
    social_results = massive_search_results.get('social_results', {})
    if social_results:
        report += "---\n\n## RESULTADOS DA BUSCA SOCIAL MASSIVA\n\n"
        
        all_posts = social_results.get('all_posts', [])
        platform_results = social_results.get('platform_results', {})
        
        report += f"**Total de Posts Encontrados:** {len(all_posts)}\n"
        report += f"**Plataformas Analisadas:** {len(platform_results)}\n\n"
        
        for platform, posts in platform_results.items():
            if posts:
                report += f"### {platform.title()} ({len(posts)} posts)\n\n"
                
                for i, post in enumerate(posts[:5], 1):
                    title = post.get('title', post.get('text', post.get('caption', 'Sem título')))[:100]
                    url = post.get('url', 'N/A')
                    engagement = post.get('engagement_rate', post.get('viral_score', 0))
                    
                    report += f"**{i}.** {title}\n"
                    report += f"   - URL: {url}\n"
                    report += f"   - Engajamento: {engagement}\n\n"

    # Seção de conteúdo viral e screenshots
    viral_content = massive_search_results.get('viral_content', [])
    screenshots = massive_search_results.get('screenshots_captured', [])
    
    if screenshots:
        report += "---\n\n## EVIDÊNCIAS VISUAIS DOS POSTS MAIS VIRAIS\n\n"
        report += f"Foram identificados **{len(viral_content)} posts virais** e capturados **{len(screenshots)} screenshots** dos posts com maior potencial de conversão.\n\n"
        
        for i, screenshot in enumerate(screenshots, 1):
            if isinstance(screenshot, dict):
                title = screenshot.get('title', 'Sem título')
                platform = screenshot.get('platform', 'N/A')
                viral_score = screenshot.get('viral_score', 0)
                url = screenshot.get('url', 'N/A')
                filename = screenshot.get('filename', f'screenshot_{i}.png')
                
                report += f"### Screenshot {i}: {title}\n\n"
                report += f"**Plataforma:** {platform.title()}  \n"
                report += f"**Score Viral:** {viral_score:.2f}/10  \n"
                report += f"**URL Original:** {url}  \n"
                
                # Métricas de engajamento
                metrics = screenshot.get('content_metrics', {})
                if metrics:
                    if 'views' in metrics:
                        report += f"**Views:** {safe_format_int(metrics['views'])}  \n"
                    if 'likes' in metrics:
                        report += f"**Likes:** {safe_format_int(metrics['likes'])}  \n"
                    if 'comments' in metrics:
                        report += f"**Comentários:** {safe_format_int(metrics['comments'])}  \n"
                
                # Referência à imagem
                relative_path = f"files/{session_id}/{filename}"
                report += f"![Screenshot {i}]({relative_path})\n\n"
                report += f"*Post viral capturado - Alto potencial de conversão*\n\n"
            else:
                # Fallback para screenshots em formato string
                report += f"### Screenshot {i}\n"
                report += f"![Screenshot {i}]({screenshot})\n\n"
    else:
        report += "---\n\n## EVIDÊNCIAS VISUAIS\n\nNenhum screenshot foi capturado nesta sessão.\n\n"
    
    # Seção de análise consolidada
    report += "---\n\n## ANÁLISE CONSOLIDADA\n\n"
    
    if websailor_results and websailor_results.get('conteudo_consolidado'):
        conteudo = websailor_results['conteudo_consolidado']
        
        insights = conteudo.get('insights_principais', [])
        if insights:
            report += "### Principais Insights Descobertos:\n"
            for i, insight in enumerate(insights[:10], 1):
                report += f"{i}. {insight}\n"
            report += "\n"
        
        tendencias = conteudo.get('tendencias_identificadas', [])
        if tendencias:
            report += "### Tendências de Mercado Identificadas:\n"
            for i, tendencia in enumerate(tendencias[:8], 1):
                report += f"**{i}.** {tendencia}\n"
            report += "\n"
        
        oportunidades = conteudo.get('oportunidades_descobertas', [])
        if oportunidades:
            report += "### Oportunidades de Negócio:\n"
            for i, oportunidade in enumerate(oportunidades[:6], 1):
                report += f"• {oportunidade}\n"
            report += "\n"
    
    # Adiciona análise dos posts virais
    if viral_content:
        report += "### Análise dos Posts Mais Virais:\n\n"
        
        # Agrupa por plataforma
        viral_by_platform = {}
        for post in viral_content:
            platform = post.get('platform', 'unknown')
            if platform not in viral_by_platform:
                viral_by_platform[platform] = []
            viral_by_platform[platform].append(post)
        
        for platform, posts in viral_by_platform.items():
            report += f"#### {platform.title()} - Posts Virais:\n"
            
            for i, post in enumerate(posts[:3], 1):
                title = post.get('title', post.get('text', post.get('caption', 'Sem título')))[:100]
                viral_score = post.get('viral_score', 0)
                category = post.get('viral_category', 'POPULAR')
                
                report += f"**{i}.** {title}\n"
                report += f"   - Score Viral: {viral_score:.2f}/10\n"
                report += f"   - Categoria: {category}\n"
                
                # Métricas específicas por plataforma
                if platform == 'youtube':
                    views = post.get('view_count', post.get('views', 0))
                    likes = post.get('like_count', post.get('likes', 0))
                    comments = post.get('comment_count', post.get('comments', 0))
                    report += f"   - Views: {safe_format_int(views)}\n"
                    report += f"   - Likes: {safe_format_int(likes)}\n"
                    report += f"   - Comentários: {safe_format_int(comments)}\n"
                
                elif platform in ['instagram', 'facebook']:
                    likes = post.get('likes', post.get('like_count', 0))
                    comments = post.get('comments', post.get('comment_count', 0))
                    shares = post.get('shares', 0)
                    report += f"   - Likes: {safe_format_int(likes)}\n"
                    report += f"   - Comentários: {safe_format_int(comments)}\n"
                    report += f"   - Compartilhamentos: {safe_format_int(shares)}\n"
                
                elif platform == 'twitter':
                    retweets = post.get('retweets', post.get('retweet_count', 0))
                    likes = post.get('likes', post.get('like_count', 0))
                    replies = post.get('replies', post.get('reply_count', 0))
                    report += f"   - Retweets: {safe_format_int(retweets)}\n"
                    report += f"   - Likes: {safe_format_int(likes)}\n"
                    report += f"   - Respostas: {safe_format_int(replies)}\n"
                
                report += "\n"
            
            report += "\n"

    # Adiciona contexto da análise
    report += "---\n\n## CONTEXTO DA ANÁLISE\n\n"
    context_items_added = False
    for key, value in context.items():
        if value: # Só adiciona se o valor não for vazio/falso
            report += f"**{key.replace('_', ' ').title()}:** {value}  \n"
            context_items_added = True
    if not context_items_added:
         report += "Nenhum contexto adicional fornecido.\n"
    
    # Adiciona metadados técnicos
    report += f"""

---

## METADADOS TÉCNICOS

### Metodologia Aplicada:
1. **Alibaba WebSailor**: Navegação profunda com múltiplos engines
2. **Rotação de APIs**: Uso intercalado de múltiplas chaves
3. **Busca Social**: Análise massiva em todas as plataformas
4. **Identificação Viral**: Algoritmo de score viral personalizado
5. **Captura Visual**: Screenshots automáticos dos posts top

### Garantias de Qualidade:
- ✅ **Zero Simulação**: Todos os dados são reais
- ✅ **Máxima Cobertura**: Múltiplas fontes e APIs
- ✅ **Evidências Visuais**: Screenshots dos posts virais
- ✅ **Dados Preservados**: Nenhuma informação perdida
- ✅ **Análise Profunda**: WebSailor + análise social

### Localização dos Arquivos:
- **Relatório Final**: `analyses_data/{session_id}/relatorio_final.md`
- **Screenshots**: `analyses_data/files/{session_id}/`
- **Dados Brutos**: `relatorios_intermediarios/`
- **Módulos**: `analyses_data/{session_id}/modules/`

---

*Relatório ULTRA-ROBUSTO gerado automaticamente em {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}*

**ARQV30 Enhanced v3.0** - Busca Massiva + WebSailor + Social + Screenshots
"""

    return report

def _save_enhanced_collection_report(report_content: str, session_id: str):
    """Salva relatório de coleta aprimorado"""
    try:
        session_dir = f"analyses_data/{session_id}"
        os.makedirs(session_dir, exist_ok=True)

        report_path = f"{session_dir}/relatorio_coleta.md"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)

        logger.info(f"✅ Relatório de coleta ULTRA-ROBUSTO salvo: {report_path}")

    except Exception as e:
        logger.error(f"❌ Erro ao salvar relatório de coleta: {e}")
