from keras import models
from keras import layers

from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Deep learning start'

    def add_arguments(self, parser):
        parser.add_argument('command', action="store", nargs='*', help='Use [ learn | predict ]')
        parser.add_argument('--verbose',action='store_true', dest='verbose', default=False, help='Set verbosity level for books collection scan.')

    def handle(self, *args, **options):
        action = options['command'][0]

        if action=='learn':
            self.stdout.write('Learning System by all having Data...')
            self.learn()
        elif action == 'predict':
            self.stdout.write('Predict for uid.')
            emp_UID = options['command'][1] if len(options['command'])>1 else None
            self.predict(emp_UID)

    def learn(self):
        print('Learning...')

        model = models.Sequential()
        model.add(layers.Dense(64, activation='relu', input_shape=(6,)))
        model.add(layers.Dense(64, activation='relu'))
        model.add(layers.Dense(46, activation='softmax'))

        model.compile(optimizer='rmsprop',
                      loss='categorical_crossentropy',
                      metrics=['accuracy'])

        # history = model.fit(x_train,
        #                     y_train,
        #                     epochs=20,
        #                     batch_size=512,
        #                     validation_data=(x_val, y_val))

    def predict(self, emp_UID):
        print('Predict for {}...'.format(emp_UID))
