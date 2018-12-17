

# rotate TOP clock wise
def T(old):
	return (old[0], old[1], old[2], old[5], old[4], old[6], old[7], old[3])

# rotate TOP counter clock wise
def rT(old):
	return (old[0], old[1], old[2], old[7], old[4], old[3], old[5], old[6])

# rotate BOTTOM clock wise
def B(old):
	return (old[4], old[0], old[1], old[3], old[2], old[5], old[6], old[7])

# rotate BOTTOM counter clock wise
def rB(old):
	return (old[1], old[2], old[4], old[3], old[0], old[5], old[6], old[7])

# fully rotate RIGHT half by 180
def R(old):
	return (old[0], old[5], old[3], old[2], old[4], old[1], old[6], old[7])

# fully rotate BOTTOM half by 180
def L(old):
	return (old[6], old[1], old[2], old[3], old[7], old[5], old[0], old[4])

def flipV(old):
	return (old[6], old[5], old[3], old[2], old[7], old[1], old[0], old[4])

def flipH(old):
	return (old[2], old[4], old[0], old[6], old[1], old[7], old[3], old[5])


# since all the possible rotations of the auzzle are basically the same combination, lets
# try to get any state to canonical form by rotating the puzzle so that 0 will be
# in the left bottom closest corner 
def getCanonical(s):
	if 0 in (s[7], s[3], s[5], s[6]):
		s = flipV(s)

	if 0 in (s[1], s[2]):
		s = flipH(s)

	return s


moves = [T, rT, B, rB, R, L]
reverseOp = {T: rT, B: rB, rB: B, rT: T, R: R, L: L}
reversePiece = {0:7, 7:0, 1:3, 3:1, 2:5, 5:2, 4:6, 6:4}
combinations = {}
initState = (0, 1, 2, 3, 4, 5, 6, 7)

def isSolved(s):
	for i in [0, 1, 2, 4]:
		if s[i] != reversePiece[s[reversePiece[i]]]:
			return False
	return True

# start with initState and perform a bfs'ish scan, every time a new state is encountered
# record it in 'combinations' dictionary along with the path length. Every time we encounter
# another solved state, we record it with depth 0 and add to queue, same for states that we've
# seen before but now with shorter pathes. There exists a more effecient algorithm for doing
# this if we start with a queue consisting of all the 'solved' permutations in the first place
def scan(maxDepth):
	q = [(initState, 0, None)]

	while len(q):
		oldState, depth, lastMove = q.pop(0)

		for move in moves:
			# optimization: ignore moves that just reverse previous move
			if lastMove != None and move == reverseOp[lastMove]:
				continue

			newState = move(oldState)
			canonical = getCanonical(newState)
			newDepth = depth + 1
			
			if isSolved(canonical):
				newDepth = 0

			if canonical in combinations:
				# we've already seen this state, did we get here faster?
				if combinations[canonical] > newDepth:
					combinations[canonical] = newDepth
					q.append((canonical, newDepth, move if newDepth != 0 else None))
			else:
				combinations[canonical] = newDepth
				if depth < maxDepth - 1:
					q.append((canonical, newDepth, move if newDepth != 0 else None))

	# iterate over all the permutations and find the maximum path
	maxpath = 0
	paths = {}
	for i in combinations:
		maxpath = max(maxpath, combinations[i])
		pathes[combinations[i]] = pathes.get(combinations[i], 0) + 1

	return maxpath, paths

maxpath, paths = scan(15)

print "Total combinations: %i, Solutions: %i, Max path to solution: %i" % (len(combinations), pathes[0], maxpath)
for i in paths:
	print "Number of paths of length %i: %i" % (i, paths[i])





