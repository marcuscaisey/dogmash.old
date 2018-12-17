def test_Dog_rank(txn, create_dog):
    dogs = [create_dog() for _ in range(4)]
    dog1, dog2, dog3, dog4 = dogs

    dog1.rating, dog2.rating, dog3.rating, dog4.rating = 1200, 900, 1000, 1000

    for dog in dogs:
        dog.save()

    assert (
        dog1.rank == 1 and dog2.rank == 3 and dog3.rank == 2 and dog4.rank == 2
    )
