from mido import MidiFile

proc_num = 1
commands = []
code = "sensor en switch1 @enabled\njump 0 notEqual en 1\ncontrol enabled switch1 0 0 0 0\n"
cur_len = 0
tempo = 5000000

mid = MidiFile("midi/march1.mid")
for i, track in enumerate(mid.tracks):
    for msg in track:
        time = msg.time * (60 / (mid.ticks_per_beat * (60000000 / tempo)))

        if msg.type == "set_tempo":
            tempo = msg.tempo

        elif msg.type == "note_on":
            if time != 0 and cur_len != 0:
                if cur_len > 0 and isinstance(commands[cur_len - 1], float):
                    commands[cur_len - 1] += time
                else:
                    commands.append(time)
                    cur_len += 1
            commands.append(f"block{msg.note - 20}")  # midi note to piano
            cur_len += 1

        elif msg.type == "note_off" and time != 0:
            if cur_len > 0 and isinstance(commands[cur_len - 1], float):
                commands[cur_len - 1] += time
            else:
                commands.append(time)
                cur_len += 1

        if cur_len > 950:
            for cmd in commands:
                code += f"control enabled {cmd} 1 0 0 0\n" if isinstance(cmd, str) else f"wait {cmd}\n"
            code += f"write 1 cell1 {proc_num + 1}\nwrite 0 cell1 {proc_num}\n"

            with open(f"code/code{proc_num}.txt", "w") as f:
                f.write(code)

            proc_num += 1
            commands = []
            cur_len = 0
            code = f"read en cell1 {proc_num}\njump 0 notEqual en 1\n"

        print(msg)

for cmd in commands:
    code += f"control enabled {cmd} 1 0 0 0\n" if isinstance(cmd, str) else f"wait {cmd}\n"
code += f"write 1 cell1 {proc_num + 1}\nwrite 0 cell1 {proc_num}\n"

with open(f"code/code{proc_num}.txt", "w") as f:
    f.write(code)

print(proc_num)
