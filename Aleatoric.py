# Aleatoric Study
# by Matthew Stein
# 11.17.2014

# Generate each note as follows:
#   (pitch, up/down, duration, played/silent),
#   where duration is a value between 1 and 16 represention sixteenth notes
#   and silent indicates that the "note" should be a rest for specified duration.

import random
from randomdotorg import RandomDotOrg
random.seed(RandomDotOrg('SeedGrabber').get_seed())

pitches = ["A", "Bb", "B", "C", "C#", "D", "Eb", "E", "F", "F#", "G", "G#"]
direction = ["up", "down"]

def randPitch():
	pitch = random.randrange(0,12)
	pitch = pitches[pitch]
	return pitch

# generate random note sequence for m measures where each measure has snpm sixteenth
# notes per measure and a lower positive integer 'silence' increases the ratio of rests
def makeMusic(m, snpm=16, silence=18, chord=True):
	piece_length = m * snpm
	filled = 0
	note_sequence = []

	while filled <= piece_length:
		if chord:
			pitches = []
			thickness = random.randrange(1,5)
			for i in range(0,thickness):
				new_pitch = randPitch()
				pitches.append(new_pitch)
		else:
			pitches = randPitch()

		move = random.randrange(0,2)
		move = direction[move]

		duration = random.randrange(1,17)
		filled += duration

		audible = random.randrange(0,silence)
		if audible == 5:
			audible = "silent"
		else:
			audible = "-"

		note_sequence.append((pitches, move, duration, audible))

	return note_sequence

print makeMusic(20)



# [('A', 'up', 10, '-'), ('C#', 'down', 8, '-'), ('F', 'down', 10, '-'), ('A', 'down', 13, '-'), ('C', 'down', 7, '-'), ('C#', 'down', 9, '-'), ('G', 'up', 5, '-'), ('F#', 'down', 16, '-'), ('F', 'down', 9, '-'), ('A', 'down', 2, '-'), ('B', 'down', 4, '-'), ('G#', 'down', 8, '-'), ('F#', 'down', 12, '-'), ('F', 'down', 8, '-'), ('C', 'up', 8, '-'), ('E', 'down', 12, 'silent'), ('B', 'down', 2, '-'), ('A', 'down', 9, '-'), ('E', 'down', 6, '-'), ('G#', 'down', 4, '-'), ('E', 'down', 3, '-'), ('E', 'down', 2, '-'), ('Bb', 'up', 5, '-'), ('F#', 'up', 9, '-'), ('D', 'down', 8, '-'), ('B', 'up', 12, '-'), ('A', 'down', 1, 'silent'), ('F', 'up', 12, '-'), ('D', 'up', 14, '-'), ('F', 'down', 15, '-')]
# [('Eb', 'down', 11, '-'), ('F#', 'down', 3, '-'), ('Eb', 'up', 14, '-'), ('C', 'down', 14, '-'), ('B', 'down', 16, '-'), ('C#', 'up', 1, '-'), ('F', 'up', 16, '-'), ('F#', 'down', 7, '-'), ('Bb', 'down', 8, '-'), ('C', 'up', 4, '-'), ('A', 'down', 8, '-'), ('Eb', 'up', 2, '-'), ('Bb', 'down', 2, '-'), ('Bb', 'down', 7, '-'), ('F#', 'up', 16, '-'), ('Bb', 'down', 6, '-'), ('G', 'down', 6, '-'), ('G#', 'down', 15, '-'), ('F', 'up', 15, '-'), ('G', 'up', 8, '-'), ('C', 'down', 10, '-'), ('F#', 'down', 11, '-'), ('C', 'up', 5, '-'), ('E', 'up', 15, '-'), ('Eb', 'down', 13, '-'), ('Bb', 'up', 7, '-'), ('A', 'down', 1, '-')]
# [('B', 'up', 11, '-'), ('C#', 'up', 5, '-'), ('F#', 'down', 10, '-'), ('C', 'up', 13, '-'), ('G#', 'up', 16, '-'), ('A', 'down', 7, '-'), ('Eb', 'down', 9, '-'), ('C#', 'up', 7, '-'), ('A', 'down', 6, '-'), ('G#', 'up', 9, '-'), ('G', 'down', 8, '-'), ('D', 'down', 15, '-'), ('G', 'up', 15, '-'), ('Bb', 'up', 11, 'silent'), ('F#', 'up', 13, '-'), ('C#', 'down', 13, '-'), ('B', 'up', 5, '-'), ('F#', 'down', 16, '-'), ('Eb', 'down', 9, '-'), ('F', 'down', 13, '-'), ('C#', 'down', 13, '-'), ('B', 'up', 8, '-'), ('A', 'down', 11, '-')]