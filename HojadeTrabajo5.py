import simpy
import random
import math

def proceso(nom, env, processcreationtime,CPU, ram, randomram, instrucciones):
    global CPUTiempo

    yield env.timeout(processcreationtime)

    horaDeRequestDeRam = env.now
    
    with ram.get(randomram) as algo:
        yield algo

        if instrucciones >= 3:
            while instrucciones >= 3:
                with CPU.request() as cola:
                    yield cola
                    yield env.timeout(1)
                    #Cambiar el numero para hacer el procesador más rapido o lento
                    instrucciones -= 3
            validador = random.randint(1, 2)
            if validador == 2:
                yield env.timeout(1)
        else:
            with CPU.request() as cola:
                yield cola
                yield env.timeout(1)
    ram.put(randomram)
    tiempoTotal = env.now - horaDeRequestDeRam
    print("%s termina su proceso a las %f" % (nom, env.now))
    CPUTiempo = CPUTiempo + tiempoTotal
    desviacion.append(tiempoTotal)

desviacion = []
env = simpy.Environment()
CPU = simpy.Resource(env, capacity = 1)
random.seed(10)
#aqui la capacidad de ram se ajusta cambiando la capacity y la init
ram = simpy.Container(env, capacity = 100, init = 100)
randomram = random.randint(1, 10)
ins = random.randint(1, 10)

#Cantidad de procesos que se crearan
cantidadDeProcesos = 25


CPUTiempo = 0


#En random.expovariate(1/10), cambiar el 10 por el intervalo deseado
for i in range(cantidadDeProcesos):
    env.process(proceso('proceso %d'%i, env, random.expovariate(1/10), CPU, ram, randomram, ins))

env.run()

print("Tiempo promedio por proceso es: ", CPUTiempo/cantidadDeProcesos)
pro = CPUTiempo/cantidadDeProcesos

algo = 0
for x in desviacion:
    algo = math.pow((x-pro), 2)
algo = algo / (cantidadDeProcesos - 1)
algo = math.sqrt(algo)

print("Desviacion estandar: ", algo)
