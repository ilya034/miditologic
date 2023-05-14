// run in mindustry console
proc = Vars.world.build(311, 152); // coord of processor
startX = 303; // coord x of left up note block
startY = 159; // coord y of left up note block
for(let i = 0; i<7; i++){
    for (let j = 0; j < 12; j++){
        x = startX + j;
        y = startY - i;
        build = Vars.world.build(x, y);
        name = proc.findLinkName(build.block);
        proc.links.add(LogicBlock.LogicLink(x, y, name, false));
    }
}