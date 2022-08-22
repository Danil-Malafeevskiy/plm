from django.contrib.auth.models import Group, AnonymousUser, User
from djangochannelsrestframework.consumers import AsyncAPIConsumer
from djangochannelsrestframework.decorators import action
from djangochannelsrestframework.observer import model_observer

from app.models import Feature, Dataset

from app.serializers import FeatureSerializer


class FeatureConsumer(AsyncAPIConsumer):
    groups = list(Group.objects.values_list("name", flat=True))

    @action()
    async def connect(self):
        if self.scope["user"] is not AnonymousUser:
            self.user_id = self.scope["user"].id
            for group in list(self.scope["user"].groups.values_list("name", flat=True)):
                await self.model_change.subscribe(group=group)
            await self.accept()

    async def disconnect(self, code):
        for group in list(self.scope["user"].groups.values_list("name", flat=True)):
            await self.model_change.unsubscribe(group=group)

    @model_observer(Feature)
    async def model_change(self, message, **kwargs):
        await  self.send_json(message)

    @model_change.serializer
    def model_change(self, instance: Feature, action, **kwargs):
        return dict(data=FeatureSerializer(instance).data, action=action.value, pk=instance.pk)

    @model_change.groups_for_signal
    def model_change(self, instance: Feature, **kwargs):
        group = Group.objects.get(id=Dataset.objects.get(id=instance.name_id).group_id).name
        yield f'-group__{group}'

    @model_change.groups_for_consumer
    def model_change(self, group=None, **kwargs):
        yield f'-group__{group}'