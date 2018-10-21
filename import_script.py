import csv
# from bookdb.models import *
import random
# from django.db import transaction
from recombee_api_client.api_client import RecombeeClient
from recombee_api_client.exceptions import APIException
from recombee_api_client.api_requests import *

client = RecombeeClient('wd-project', 'DDf4VljyLxNsbdLtWT1jueFbVsanOWCwbEW59cTpp1W3LB3JlpeT3jqZQ1k7S7sN')

# @transaction.atomic
# def main():
# 	with open('BX-CSV-Dump/BX-Users.csv', encoding='utf-8') as f:
# 		reader = list(csv.reader(f, delimiter=';'))

# 		# Skipping the headers
# 		# next(reader)
# 		print("Result =", len(reader))
# 		count = 0
# 		# transaction.set_autocommit(False)
# 		with transaction.atomic():
# 			for row in reader[1:]:
# 				count += 1
# 				# if User.objects.filter(id=int(row[0])).count() == 0:
# 				user = User(id=int(row[0]))
# 				user.username = str(user.id)
# 				user.set_password('pass@123')
# 				user.is_superuser = True
# 				user.is_staff = True
# 				user.save()
# 					# profile = UserProfile(user=user)
# 					# profile.save()
# 				print(count)
# 			# if count == 1000:
# 			# 	transaction.commit()
# 		# 	if count == 50000:
# 		# 		transaction.commit()
# 		# transaction.commit()

def main():
	requests = []
	with open('BX-CSV-Dump/BX-Book-Ratings.csv', encoding='utf-8') as f:
		reader = list(csv.reader(f, delimiter=';'))[1000:6000]
		for row in reader:
			request = AddRating(row[0], row[1], (int(row[2])-5)/5, cascade_create=True)
			requests.append(request)
	try:
		print('Send Ratings')
		client.send(Batch(requests))
	except APIException as e:
		print(e)

# main()

recommended = client.send(RecommendItemsToUser('276747', 5))
print(recommended)

# transaction.set_autocommit(True)
