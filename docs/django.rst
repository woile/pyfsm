Django integration
==================

.. code-block:: python

    import fsm
    from django.db import models


    class MyModel(models.Model, fsm.FiniteStateMachineMixin):
        """An example to test the state machine.

        Contains transitions to everywhere, nowhere and specific states.
        """

        CHOICES = (
            ('created', 'CREATED'),
            ('pending', 'PENDING'),
            ('running', 'RUNNING'),
            ('success', 'SUCCESS'),
            ('failed', 'FAILED'),
            ('retry', 'RETRY'),
        )

        state_machine = {
            'created': '__all__',
            'pending': ('running',),
            'running': ('success', 'failed'),
            'success': None,
            'failed': ('retry',),
            'retry': ('pending', 'retry'),
        }

        state = models.CharField(max_length=30, choices=CHOICES, default='created')

        def on_change_state(self, previous_state, next_state, **kwargs):
            self.save()

Django Rest Framework
---------------------

If you are using :code:`serializers`, they usually perform the :code:`save`, so saving inside :code:`on_change_state` is not necessary.

One simple solution is to do this:

.. code-block:: python

    class MySerializer(serializers.ModelSerializer):

        def update(self, instance, validated_data):
            new_state = validated_data.get('state', instance.state)
            try:
                instance.change_state(new_state)
            except fsm.InvalidTransition:
                raise serializers.ValidationError("Invalid transition")
            instance = super().update(instance, validated_data)
            return instance
