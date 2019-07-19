import time
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

    def predict(self, emp_UID):
        print('Predict for {}...'.format(emp_UID))
