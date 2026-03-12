# Este é o "coração" do WebSocket — recebe e envia mensagens em tempo real

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Conversa, Mensagem


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        """Chamado quando o usuário abre o chat"""
        self.conversa_id = self.scope['url_route']['kwargs']['conversa_id']
        self.room_group_name = f'chat_{self.conversa_id}'
        self.user = self.scope['user']

        # Verifica se o usuário tem acesso a essa conversa
        if not await self.tem_acesso():
            await self.close()
            return

        # Entra no grupo da conversa
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        """Chamado quando o usuário fecha o chat"""
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """Chamado quando o usuário envia uma mensagem"""
        data = json.loads(text_data)
        texto = data.get('texto', '').strip()

        if not texto:
            return

        # Salva a mensagem no banco de dados
        mensagem = await self.salvar_mensagem(texto)

        # Envia para todos no grupo (cliente + prestador)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'mensagem_id': mensagem.id,
                'texto': mensagem.texto,
                'autor_id': self.user.id,
                'autor_nome': self.user.username,
                'enviada_em': mensagem.enviada_em.strftime('%H:%M'),
            }
        )

    async def chat_message(self, event):
        """Envia a mensagem para o WebSocket do cliente"""
        await self.send(text_data=json.dumps(event))

    # -------------------------------------------------------
    # Métodos auxiliares (rodam de forma assíncrona)
    # -------------------------------------------------------

    @database_sync_to_async
    def tem_acesso(self):
        try:
            conversa = Conversa.objects.get(id=self.conversa_id)
            return self.user in [conversa.cliente, conversa.prestador]
        except Conversa.DoesNotExist:
            return False

    @database_sync_to_async
    def salvar_mensagem(self, texto):
        conversa = Conversa.objects.get(id=self.conversa_id)
        return Mensagem.objects.create(
            conversa=conversa,
            autor=self.user,
            texto=texto
        )