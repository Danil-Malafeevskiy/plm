from django.contrib.auth.models import Group, AnonymousUser, User
from djangochannelsrestframework.consumers import AsyncAPIConsumer
from djangochannelsrestframework.decorators import action
from djangochannelsrestframework.observer import model_observer

from app.models import Feature

from app.serializers import FeatureSerializer


class FeatureConsumer(AsyncAPIConsumer):
    groups = list(Group.objects.values_list("name", flat=True))

    @action()
    async def connect(self):
        if self.scope["user"] is not AnonymousUser:
            self.user_id = self.scope["user"].id
            await self.channel_layer.group_add(self.scope["user"].groups.values_list("name", flat=True).first(), self.channel_name)
            await self.accept()

    async def accept(self, **kwargs):
        await super().accept(**kwargs)
        await self.model_change.subscribe(group=self.scope["user"].groups.values_list("name", flat=True).first())

    async def disconnect(self, code):
        group_name = self.scope["user"].groups.values_list("name", flat=True).first()
        await self.channel_layer.group_discard(group_name, self.channel_name)

    @model_observer(Feature)
    async def model_change(self, message, **kwargs):
        await  self.send_json(message)

    @model_change.serializer
    def model_change(self, instance: Feature, action, **kwargs):
        return dict(data=FeatureSerializer(instance).data, action=action.value, pk=instance.pk)

    @model_change.groups_for_signal
    def model_change(self, instance: Feature, **kwargs):
        yield f'-group__{instance.group}'

    @model_change.groups_for_consumer
    def model_change(self, group=None, **kwargs):
        yield f'-group__{group}'