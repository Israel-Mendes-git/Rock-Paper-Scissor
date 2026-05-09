import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import random
import os

# Cores - paleta mais moderna
COR_FUNDO = "#1a1a2e"
COR_PRIMARIA = "#16213e"
COR_SECUNDARIA = "#0f3460"
COR_DESTAQUE = "#e94560"
COR_TEXTO = "#ffffff"
COR_VERDE = "#4caf50"
COR_VERMELHO = "#f44336"
COR_AMARELO = "#ffd700"
COR_CINZA = "#9e9e9e"

class JogoPedraPapelTesoura:
    def __init__(self):
        self.janela = tk.Tk()
        self.janela.title("Pedra, Papel e Tesoura")
        self.janela.geometry("500x600")
        self.janela.configure(bg=COR_FUNDO)
        self.janela.resizable(False, False)
        
        # Centralizar janela
        self.centralizar_janela()
        
        # Variáveis do jogo
        self.pontos_voce = 0
        self.pontos_pc = 0
        self.rondas = 5
        self.rondas_jogadas = 0
        
        # Inicializar mixer de som (opcional)
        self.som_ativado = True
        try:
            self.criar_sons()
        except:
            self.som_ativado = False
        
        # Dicionário de escolhas
        self.escolhas = {
            "Pedra": {"emoji": "🪨", "cor": COR_CINZA},
            "Papel": {"emoji": "📄", "cor": "#2196f3"},
            "Tesoura": {"emoji": "✂️", "cor": COR_VERMELHO}
        }
        
        # Configurar interface
        self.configurar_estilo()
        self.criar_widgets()
        
    def centralizar_janela(self):
        """Centraliza a janela na tela"""
        self.janela.update_idletasks()
        largura = self.janela.winfo_width()
        altura = self.janela.winfo_height()
        x = (self.janela.winfo_screenwidth() // 2) - (largura // 2)
        y = (self.janela.winfo_screenheight() // 2) - (altura // 2)
        self.janela.geometry(f'{largura}x{altura}+{x}+{y}')
    
    def criar_sons(self):
        """Cria efeitos sonoros (opcional)"""
        # Você pode adicionar arquivos .wav para os sons
        self.som_clique = None
        self.som_vitoria = None
        self.som_derrota = None
        
    def configurar_estilo(self):
        """Configura o estilo dos widgets"""
        style = ttk.Style(self.janela)
        style.theme_use('clam')
        
        # Configurar botões
        style.configure('Jogo.TButton', 
                       font=('Helvetica', 12, 'bold'),
                       padding=10)
        
    def criar_widgets(self):
        """Cria todos os widgets da interface"""
        # Frame superior (placar)
        self.frame_cima = tk.Frame(self.janela, bg=COR_PRIMARIA, height=150)
        self.frame_cima.pack(fill=tk.X, padx=20, pady=20)
        self.frame_cima.pack_propagate(False)
        
        # Placar
        self.criar_placar()
        
        # Frame do meio (resultados)
        self.frame_meio = tk.Frame(self.janela, bg=COR_FUNDO, height=150)
        self.frame_meio.pack(fill=tk.X, padx=20, pady=10)
        self.frame_meio.pack_propagate(False)
        
        # Labels para mostrar as escolhas
        self.escolha_voce_label = tk.Label(self.frame_meio, text="?", font=('Arial', 48), 
                                          bg=COR_FUNDO, fg=COR_TEXTO)
        self.escolha_voce_label.pack(side=tk.LEFT, expand=True)
        
        self.vs_label = tk.Label(self.frame_meio, text="VS", font=('Arial', 24, 'bold'), 
                                bg=COR_FUNDO, fg=COR_DESTAQUE)
        self.vs_label.pack(side=tk.LEFT, expand=True)
        
        self.escolha_pc_label = tk.Label(self.frame_meio, text="?", font=('Arial', 48), 
                                        bg=COR_FUNDO, fg=COR_TEXTO)
        self.escolha_pc_label.pack(side=tk.LEFT, expand=True)
        
        # Label do resultado
        self.resultado_label = tk.Label(self.janela, text="Clique em Jogar para começar!", 
                                       font=('Helvetica', 14, 'bold'), 
                                       bg=COR_FUNDO, fg=COR_AMARELO)
        self.resultado_label.pack(pady=20)
        
        # Frame dos botões
        self.frame_botoes = tk.Frame(self.janela, bg=COR_FUNDO)
        self.frame_botoes.pack(pady=20)
        
        # Botão Jogar
        self.botao_jogar = tk.Button(self.frame_botoes, text="🎮 JOGAR", 
                                    command=self.iniciar_jogo,
                                    font=('Helvetica', 14, 'bold'),
                                    bg=COR_DESTAQUE, fg=COR_TEXTO,
                                    width=15, height=2,
                                    relief=tk.RAISED, bd=3,
                                    cursor="hand2")
        self.botao_jogar.pack()
        
        # Frame de status
        self.frame_status = tk.Frame(self.janela, bg=COR_FUNDO)
        self.frame_status.pack(fill=tk.X, padx=20, pady=10)
        
        self.status_label = tk.Label(self.frame_status, 
                                    text=f"Rodada: 0/{self.rondas}", 
                                    font=('Helvetica', 10),
                                    bg=COR_FUNDO, fg=COR_CINZA)
        self.status_label.pack()
        
    def criar_placar(self):
        """Cria o placar do jogo"""
        # Frame para o placar
        placar_frame = tk.Frame(self.frame_cima, bg=COR_PRIMARIA)
        placar_frame.pack(expand=True)
        
        # Você
        voce_frame = tk.Frame(placar_frame, bg=COR_PRIMARIA)
        voce_frame.pack(side=tk.LEFT, padx=40)
        
        tk.Label(voce_frame, text="VOCÊ", font=('Helvetica', 14, 'bold'),
                bg=COR_PRIMARIA, fg=COR_TEXTO).pack()
        
        self.pontos_voce_label = tk.Label(voce_frame, text="0", 
                                         font=('Helvetica', 48, 'bold'),
                                         bg=COR_PRIMARIA, fg=COR_VERDE)
        self.pontos_voce_label.pack()
        
        # Separador
        tk.Label(placar_frame, text=":", font=('Helvetica', 48, 'bold'),
                bg=COR_PRIMARIA, fg=COR_TEXTO).pack(side=tk.LEFT, padx=20)
        
        # Computador
        pc_frame = tk.Frame(placar_frame, bg=COR_PRIMARIA)
        pc_frame.pack(side=tk.LEFT, padx=40)
        
        tk.Label(pc_frame, text="PC", font=('Helvetica', 14, 'bold'),
                bg=COR_PRIMARIA, fg=COR_TEXTO).pack()
        
        self.pontos_pc_label = tk.Label(pc_frame, text="0", 
                                       font=('Helvetica', 48, 'bold'),
                                       bg=COR_PRIMARIA, fg=COR_VERMELHO)
        self.pontos_pc_label.pack()
        
    def carregar_imagens(self):
        """Carrega as imagens dos botões"""
        try:
            imagens = {}
            for escolha in self.escolhas.keys():
                # Tentar carregar imagem, se não existir, usar emoji
                caminho = f'imagens/{escolha.lower()}.png'
                if os.path.exists(caminho):
                    img = Image.open(caminho)
                    img = img.resize((60, 60), Image.Resampling.LANCZOS)
                    imagens[escolha] = ImageTk.PhotoImage(img)
                else:
                    imagens[escolha] = None
            return imagens
        except:
            return {escolha: None for escolha in self.escolhas.keys()}
    
    def iniciar_jogo(self):
        """Inicia uma nova partida"""
        self.pontos_voce = 0
        self.pontos_pc = 0
        self.rondas_jogadas = 0
        self.atualizar_placar()
        self.resultado_label.config(text="Faça sua escolha!", fg=COR_VERDE)
        
        # Destruir botão jogar
        self.botao_jogar.destroy()
        
        # Criar botões de escolha
        self.criar_botoes_escolha()
        
    def criar_botoes_escolha(self):
        """Cria os botões para as escolhas do jogador"""
        # Limpar frame de botões
        for widget in self.frame_botoes.winfo_children():
            widget.destroy()
        
        # Carregar imagens
        imagens = self.carregar_imagens()
        
        # Criar botões
        for escolha in self.escolhas.keys():
            emoji = self.escolhas[escolha]["emoji"]
            cor = self.escolhas[escolha]["cor"]
            
            # Se tiver imagem, usar imagem, senão usar texto com emoji
            if imagens[escolha]:
                botao = tk.Button(self.frame_botoes, 
                                 image=imagens[escolha],
                                 command=lambda e=escolha: self.jogar(e),
                                 bg=COR_SECUNDARIA,
                                 relief=tk.RAISED, bd=3,
                                 cursor="hand2")
                botao.image = imagens[escolha]  # Manter referência
            else:
                botao = tk.Button(self.frame_botoes, 
                                 text=f"{emoji}\n{escolha}",
                                 command=lambda e=escolha: self.jogar(e),
                                 font=('Helvetica', 12, 'bold'),
                                 bg=COR_SECUNDARIA, fg=COR_TEXTO,
                                 width=8, height=3,
                                 relief=tk.RAISED, bd=3,
                                 cursor="hand2")
            
            botao.pack(side=tk.LEFT, padx=10)
        
        # Botão de reiniciar
        tk.Button(self.frame_botoes, text="🔄 Reiniciar",
                 command=self.reiniciar_jogo,
                 font=('Helvetica', 10, 'bold'),
                 bg=COR_CINZA, fg=COR_TEXTO,
                 width=8, height=3,
                 relief=tk.RAISED, bd=3,
                 cursor="hand2").pack(side=tk.LEFT, padx=10)
        
    def jogar(self, escolha_voce):
        """Executa uma jogada"""
        # Verificar se o jogo acabou
        if self.rondas_jogadas >= self.rondas:
            self.fim_de_jogo()
            return
        
        # Escolha do computador
        escolha_pc = random.choice(list(self.escolhas.keys()))
        
        # Atualizar labels com as escolhas
        emoji_voce = self.escolhas[escolha_voce]["emoji"]
        emoji_pc = self.escolhas[escolha_pc]["emoji"]
        
        self.escolha_voce_label.config(text=f"{emoji_voce}\n{escolha_voce}")
        self.escolha_pc_label.config(text=f"{emoji_pc}\n{escolha_pc}")
        
        # Determinar vencedor
        resultado = self.determinar_vencedor(escolha_voce, escolha_pc)
        
        # Atualizar pontuação
        if resultado == "voce":
            self.pontos_voce += 1
            mensagem = "🎉 Você ganhou esta rodada! 🎉"
            cor_resultado = COR_VERDE
            self.animar_vitoria()
        elif resultado == "pc":
            self.pontos_pc += 1
            mensagem = "💻 Computador ganhou esta rodada! 💻"
            cor_resultado = COR_VERMELHO
            self.animar_derrota()
        else:
            mensagem = "🤝 Empate! 🤝"
            cor_resultado = COR_AMARELO
            self.animar_empate()
        
        # Atualizar placar e status
        self.atualizar_placar()
        self.rondas_jogadas += 1
        self.status_label.config(text=f"Rodada: {self.rondas_jogadas}/{self.rondas}")
        
        # Mostrar resultado
        self.resultado_label.config(text=mensagem, fg=cor_resultado)
        
        # Verificar se o jogo acabou
        if self.rondas_jogadas >= self.rondas:
            self.janela.after(1500, self.fim_de_jogo)
    
    def determinar_vencedor(self, voce, pc):
        """Determina o vencedor da rodada"""
        # Regras do jogo
        regras = {
            "Pedra": "Tesoura",
            "Papel": "Pedra", 
            "Tesoura": "Papel"
        }
        
        if voce == pc:
            return "empate"
        elif regras[voce] == pc:
            return "voce"
        else:
            return "pc"
    
    def animar_vitoria(self):
        """Animação para vitória"""
        self.janela.configure(bg=COR_VERDE)
        self.janela.after(300, lambda: self.janela.configure(bg=COR_FUNDO))
        
    def animar_derrota(self):
        """Animação para derrota"""
        self.janela.configure(bg=COR_VERMELHO)
        self.janela.after(300, lambda: self.janela.configure(bg=COR_FUNDO))
        
    def animar_empate(self):
        """Animação para empate"""
        self.janela.configure(bg=COR_AMARELO)
        self.janela.after(300, lambda: self.janela.configure(bg=COR_FUNDO))
    
    def atualizar_placar(self):
        """Atualiza o placar na interface"""
        self.pontos_voce_label.config(text=str(self.pontos_voce))
        self.pontos_pc_label.config(text=str(self.pontos_pc))
    
    def fim_de_jogo(self):
        """Mostra o resultado final do jogo"""
        # Destruir botões de escolha
        for widget in self.frame_botoes.winfo_children():
            widget.destroy()
        
        # Determinar vencedor final
        if self.pontos_voce > self.pontos_pc:
            mensagem = f"🏆 GG! Você venceu por {self.pontos_voce} a {self.pontos_pc}! 🏆"
            cor = COR_VERDE
        elif self.pontos_voce < self.pontos_pc:
            mensagem = f"😭 Melhore! Você perdeu por {self.pontos_pc} a {self.pontos_voce}... 😭"
            cor = COR_VERMELHO
        else:
            mensagem = f"🤝 EMPATE! Placar final: {self.pontos_voce} a {self.pontos_pc} 🤝"
            cor = COR_AMARELO
        
        self.resultado_label.config(text=mensagem, fg=cor, font=('Helvetica', 12, 'bold'))
        
        # Botão para jogar novamente
        tk.Button(self.frame_botoes, text="🎮 JOGAR NOVAMENTE 🎮",
                 command=self.reiniciar_jogo,
                 font=('Helvetica', 14, 'bold'),
                 bg=COR_DESTAQUE, fg=COR_TEXTO,
                 width=20, height=2,
                 relief=tk.RAISED, bd=3,
                 cursor="hand2").pack(pady=20)
        
        # Botão para sair
        tk.Button(self.frame_botoes, text="🚪 SAIR",
                 command=self.janela.quit,
                 font=('Helvetica', 12, 'bold'),
                 bg=COR_VERMELHO, fg=COR_TEXTO,
                 width=10, height=1,
                 relief=tk.RAISED, bd=3,
                 cursor="hand2").pack(pady=5)
    
    def reiniciar_jogo(self):
        """Reinicia o jogo completamente"""
        # Resetar variáveis
        self.pontos_voce = 0
        self.pontos_pc = 0
        self.rondas_jogadas = 0
        
        # Limpar interfaces
        for widget in self.frame_botoes.winfo_children():
            widget.destroy()
        for widget in self.frame_cima.winfo_children():
            widget.destroy()
        for widget in self.frame_meio.winfo_children():
            widget.destroy()
        
        # Recriar widgets
        self.criar_placar()
        
        # Resetar labels de escolha
        self.escolha_voce_label = tk.Label(self.frame_meio, text="?", font=('Arial', 32), 
                                          bg=COR_FUNDO, fg=COR_TEXTO)
        self.escolha_voce_label.pack(side=tk.LEFT, expand=True)
        
        self.vs_label = tk.Label(self.frame_meio, text="VS", font=('Arial', 24, 'bold'), 
                                bg=COR_FUNDO, fg=COR_DESTAQUE)
        self.vs_label.pack(side=tk.LEFT, expand=True)
        
        self.escolha_pc_label = tk.Label(self.frame_meio, text="?", font=('Arial', 32), 
                                        bg=COR_FUNDO, fg=COR_TEXTO)
        self.escolha_pc_label.pack(side=tk.LEFT, expand=True)
        
        self.resultado_label.config(text="Clique em Jogar para começar!", fg=COR_AMARELO)
        
        # Recriar botão jogar
        self.botao_jogar = tk.Button(self.frame_botoes, text="🎮 JOGAR", 
                                    command=self.iniciar_jogo,
                                    font=('Helvetica', 14, 'bold'),
                                    bg=COR_DESTAQUE, fg=COR_TEXTO,
                                    width=15, height=2,
                                    relief=tk.RAISED, bd=3,
                                    cursor="hand2")
        self.botao_jogar.pack()
        
        self.status_label.config(text=f"Rodada: 0/{self.rondas}")
        
    def executar(self):
        """Executa o jogo"""
        self.janela.mainloop()

# Executar o jogo
if __name__ == "__main__":
    jogo = JogoPedraPapelTesoura()
    jogo.executar()