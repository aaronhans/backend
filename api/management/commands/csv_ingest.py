from django.core.management.base import BaseCommand
from django.core import management
import csv

from api.models import Location, Hour


class Command(BaseCommand):
    help = 'Ingests data into the db from csv_files. This command will kill and fill the api_location and api_hours tables.'

    def handle(self, *args, **options):
        Location.objects.all().delete()
        Hour.objects.all().delete()
        csv_files = ['farmers-market.csv',
                     'community_gardens.csv', 'food-pantry.csv', 'supermarket.csv']
        location_count = 0
        for file in csv_files:
            try:
                with open('csv_files/{}'.format(file), 'r') as f:
                    reader = csv.reader(f)
                    next(f)
                    for r in reader:
                        loc = Location(name=r[0],
                                       address_1=r[1],
                                       address_2=r[2],
                                       city=r[3],
                                       state=r[4],
                                       zipcode=r[5],
                                       phone=r[6],
                                       latitude=r[7],
                                       longitude=r[8],
                                       category=r[9],
                                       website=r[10],
                                       active=True)
                        loc.save()
                        hours = list(filter(None, r[11:]))
                        for i in range(0, len(hours), 3):
                            day, open_time, close_time = hours[i:i + 3]
                            hour = Hour(day=day,
                                        open_time=self._format_time(open_time),
                                        close_time=self._format_time(
                                            close_time),
                                        location=loc)
                            hour.save()
                        location_count += 1

            except:
                self.stdout.write(
                    "Not all rows loaded to the database. The last row loaded was {0} {1}. The ingest failed in file {2}".format(loc.name, loc.address_1, file))

        self.stdout.write(
            "{} locations have been added to the database.".format(location_count))

    def _format_time(self, time):
        time_list = list(time)
        time_list.insert(-2, ':')
        return ''.join(time_list)
