# botao de iniciar chat
# popup para entrar no site
# quando entrar no chat: (aparece para todo mundo)
    #aparecer mensagem que você entrou no chat
# a cada mensagem que você envia (aparece para todo mundo)
    # Nome: Texto da mensagem

{

}

import flet as ft

def main(pagina):
    texto = ft.Text("Hashzap")

    chat = ft.Column()

    nome_usuario = ft.TextField(label="Escreva seu nome")

    def enviar_mensagem_tunel(mensagem):
        tipo = mensagem["tipo"]
        if tipo == "mensagem":
            texto_mensagem = mensagem["texto"]
            usuario_mensagem = mensagem["usuario"]
            chat.controls.append(ft.Text(f"{usuario_mensagem}: {texto_mensagem}", color=ft.colors.WHITE))
        else:
            usuario_mensagem = mensagem["usuario"]    
            chat.controls.append(ft.Text(f"{usuario_mensagem} entrou no chat", size=20, italic=True, color=ft.colors.RED_500))
        pagina.update()
 
    pagina.pubsub.subscribe(enviar_mensagem_tunel)

    def enviar_mensagem(evento):
        pagina.pubsub.send_all({"texto": campo_mensagem.value, "usuario": nome_usuario.value, "tipo": "mensagem"})

        campo_mensagem.value = ""
        pagina.update()

    campo_mensagem = ft.TextField(label="Digite uma mensagem", on_submit=enviar_mensagem)
    botao_enviar_mensagem = ft.ElevatedButton("Enviar", on_click=enviar_mensagem)

    def entrar_popup(evento):
        pagina.pubsub.send_all({"usuario": nome_usuario.value, "tipo": "entrada"})
        # adicionar o chat
        pagina.add(chat)
        # fechar o popup
        popup.open = False
        # remover botão iniciar chat
        pagina.remove(botao_iniciar)
        pagina.remove(texto)
        # criar campo de mensagem do usuário
        pagina.add(ft.Row(
            [campo_mensagem, botao_enviar_mensagem]
            ))
        # Criar o botão de enviar mensagem do usuário
        pagina.update()

    popup = ft.AlertDialog(
        open=False,
        modal=True,
        title=ft.Text("Bem-vindo ao HashZap"),
        content=nome_usuario,
        actions=[ft.ElevatedButton("Entrar", on_click=entrar_popup)]
    )

    def entrar_chat(evento):
        pagina.dialog = popup
        popup.open = True
        pagina.update()

    botao_iniciar = ft.ElevatedButton("Iniciar chat", on_click=entrar_chat)

    pagina.add(texto)
    pagina.add(botao_iniciar)

ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=8080)