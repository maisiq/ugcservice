sh.addShard("mongors1/mongors1n1:27017");
sh.addShard("mongors2/mongors2n1:27017");
sh.shardCollection("movies.movies", { _id: "hashed" }, { numInitialChunks: 5 });

