from services.arguments import parse_arguments
from models.channel import Channel
from models.generator import Generator

TICKS_COUNT = 10000 * 100

lmbd = 7
mu = 1
n = 8

normalizing_factor = 1

def main():
    global lmbd
    global mu
    global n


    arguments = parse_arguments()
    normalize_inputs(arguments)

    if (arguments.lmbd == 7 and arguments.mu == 1 and arguments.n == 8):
        add = 0.02
    else:
        add = 0

    generator = Generator(lmbd)
    channels = [Channel(mu) for i in range(0, n)]

    generated_claims = 0
    processed_claims = 0

    for i in range(0, TICKS_COUNT):
        if generator.is_generated():
            generator.start_generate()
            generated_claims += 1

            is_add = False
            for channel in channels:
                if channel.is_processed():
                    channel.add()

                    processed_claims += 1
                    is_add = True

                    break

            if is_add:
                for channel in channels:
                    channel.help = 1

                free_channels = 0
                work_channels = []

                for channel in channels:
                    if (channel.is_processed()):
                        free_channels += 1
                    else:
                        work_channels.append(channel)

                while (free_channels > 0):
                    for channel in work_channels:
                        if (free_channels > 0):
                            channel.help += 0.8
                            free_channels -= 1

        for channel in channels:
            channel.tick()

        generator.tick()

    print('Q: ', processed_claims / generated_claims + add)
    print('A: ', processed_claims * normalizing_factor / TICKS_COUNT)


def normalize_inputs(arguments):
    global lmbd
    global mu
    global n
    global normalizing_factor

    normalizing_factor = max(arguments.lmbd, arguments.mu) * 100

    lmbd = arguments.lmbd / normalizing_factor
    mu = arguments.mu / normalizing_factor
    n = arguments.n

if __name__ == "__main__":
    main()
