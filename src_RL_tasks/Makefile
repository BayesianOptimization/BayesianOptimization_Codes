EXPDIR=./$(shell date +%F)
ZACQ=EI
BUDGET=200
RUNS=199
NOISEMEAN=0.0
NOISEVAR=0.25
NUMRESTARTS=10
RAWSAMPLES=32
RANDOMSEED=42
INIT_EXAMPLES=5
NUM_FANTASIES=128
ARGS=$(EXPDIR) $(ZACQ) $(BUDGET) $(RUNS) $(NOISEMEAN) $(NOISEVAR) $(NUMRESTARTS) $(RAWSAMPLES) $(RANDOMSEED) $(INIT_EXAMPLES) $(NUM_FANTASIES)

basic:
	chmod +x run.sh

le_branke: basic
	./run.sh le_branke max 1 $(ARGS)
# python3 post_process.py -e $(EXPDIR)/le_branke/ -s 0.1 -x Number\ of\ Iterations -y Mean\ Regret

all: basic
	./run.sh cart_pole max 30 $(ARGS)
	python3 post_process.py -e $(EXPDIR)/cart_pole/ -s 0.1 -x Number\ of\ Iterations -y Mean\ Regret
# ./run.sh pongChangeMountainCar min 25 $(ARGS)
# ./run.sh lunar_lander max 192 $(ARGS)
	./run.sh gw max 20 $(ARGS)
	python3 post_process.py -e $(EXPDIR)/gw/ -s 0.1 -x Number\ of\ Iterations -y Mean\ Regret
# Cosine8: basic
# ./run.sh Cosine8 max 8 $(ARGS)
# python3 post_process.py -e $(EXPDIR)/Cosine8/ -s 0.1 -x Number\ of\ Iterations -y Mean\ Regret
gwave: basic
#	./run.sh Drop_Wave min 2 $(ARGS)
# # python3 post_process.py -e $(EXPDIR)/Drop_Wave/ -s 0.1 -x Number\ of\ Iterations -y Mean\ Regret

# StyblinskiTang: basic
# ./run.sh StyblinskiTang min 4 $(ARGS)
# # python3 post_process.py -e $(EXPDIR)/StyblinskiTang/ -s 0.1 -x Number\ of\ Iterations -y Mean\ Regret

# DixonPrice: basic
# ./run.sh DixonPrice min 5 $(ARGS)
# # python3 post_process.py -e $(EXPDIR)/DixonPrice/ -s 0.1 -x Number\ of\ Iterations -y Mean\ Regret

# SixHumpCamel: basic
#	./run.sh SixHumpCamel min 2 $(ARGS)
# # python3 post_process.py -e $(EXPDIR)/SixHumpCamel/ -s 0.1 -x Number\ of\ Iterations -y Mean\ Regret

# ThreeHumpCamel: basic
#	./run.sh ThreeHumpCamel min 2 $(ARGS)
# # python3 post_process.py -e $(EXPDIR)/ThreeHumpCamel/ -s 0.1 -x Number\ of\ Iterations -y Mean\ Regret

# Sphere: basic
# ./run.sh Sphere min 6 $(ARGS)
# # python3 post_process.py -e $(EXPDIR)/Sphere/ -s 0.1 -x Number\ of\ Iterations -y Mean\ Regret

# Bukin: basic
#	./run.sh Bukin min 2 $(ARGS)
# python3 post_process.py -e $(EXPDIR)/Bukin/ -s 0.1 -x Number\ of\ Iterations -y Mean\ Regret

# Griewank: basic
#	./run.sh Griewank min 6 $(ARGS)
# python3 post_process.py -e $(EXPDIR)/Griewank/ -s 0.1 -x Number\ of\ Iterations -y Mean\ Regret

# Michalewicz: basic
#	./run.sh Michalewicz min 10 $(ARGS)
# python3 post_process.py -e $(EXPDIR)/Michalewicz/ -s 0.1 -x Number\ of\ Iterations -y Mean\ Regret

# Sum_exp: basic
# ./run.sh Sum_exp min 6 $(ARGS)
# python3 post_process.py -e $(EXPDIR)/Sum_exp/ -s 0.1 -x Number\ of\ Iterations -y Mean\ Regret
