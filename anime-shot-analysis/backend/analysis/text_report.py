def generate_shot_explanation(shot_type, pos, scale, tone, comp, palette):

    parts = []

    if shot_type and shot_type!="unknown":
        st = {"CU":"Close-Up","MS":"Medium Shot","LS":"Long Shot"}.get(shot_type,shot_type)
        parts.append(f"This shot is a {st}, emphasizing character presence and storytelling intent.")

    if pos:
        p = {"left":"left-weighted","center":"centered","right":"right-weighted"}.get(pos,pos)
        parts.append(f"The composition is {p}, guiding viewer attention.")

    if scale:
        parts.append(f"The subject scale is {scale.lower()}, affecting narrative importance.")

    if comp:
        parts.append(f"Framing bias leans toward the {comp.lower()} region.")

    if tone:
        t = {"cool":"cool tones", "warm":"warm tones","neutral":"neutral tones"}.get(tone,tone)
        parts.append(f"The palette uses {t}, shaping mood and atmosphere.")

    if palette:
        parts.append("Overall, the color scheme reinforces the emotional direction of the scene.")

    if len(parts)==0:
        return "The system could not identify elements due to low detection confidence."

    return " ".join(parts)