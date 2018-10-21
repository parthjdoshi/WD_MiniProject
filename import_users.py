import csv
from bookdb.models import *
import random
from django.db import transaction

@transaction.atomic
def main():
	with open('BX-CSV-Dump/BX-Book-Ratings.csv', encoding='utf-8') as f:
		reader = list(csv.reader(f, delimiter=';'))[1:6000]
		count = 0
		for row in reader:
			count += 1
			user, created = User.objects.get_or_create(id=int(row[0]))
			if created:
				user.username = row[0]
				user.set_password('pass@123')
				user.first_name = random.choice(['Fenil', 'Akshat', 'Khushmann', 'Parth'])
				user.last_name = random.choice(['Doshi', 'Jain', 'Dwivedi'])
				user.save()
				profile = UserProfile(user=user)
				profile.save()
			book, created = Book.objects.get_or_create(isbn=row[1])
			book.save()
			rating, created = Rating.objects.get_or_create(user=profile, book=book)
			if not created:
				rating.rating = int(row[2])
			rating.save()
			print(count)

main()
