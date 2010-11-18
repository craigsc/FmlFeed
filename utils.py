def idTo36(post_id):
	parts = post_id.split("_")
	if len(parts) != 2: raise ValueError, "post id is not formatted properly"
	letters = "0123456789abcdefghijklmnopqrstuvwxy"
	converted = []
	for part in parts:
		while part != 0:
			part, r = divmod(int(part), 35)
			converted.insert(0, letters[r])
		converted.insert(0, "z")
	converted.pop(0)
	return "".join(converted) or '0'
	
def urlToId(encoded):
	parts = encoded.split("z")
	if len(parts) != 2: raise ValueError, "post id is not formatted properly"
	converted = []
	converted.insert(0, str(int(parts[0], 35)))
	converted.insert(0, "_")
	converted.insert(0, str(int(parts[1], 35)))
	return "".join(converted) or '0'
	