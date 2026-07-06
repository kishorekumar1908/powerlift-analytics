from lookup import get_all_lookups

lookups = get_all_lookups()

print()

for name, lookup in lookups.items():

    print(name, len(lookup))