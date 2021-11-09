
class BoggleGame{

    constructor(container, time){
        this.board = $(container);
        this.time = time;
    }

}

//create game instance only when board page is loaded
if ($('.boardPage').length){
    const game = new BoggleGame('.boardPage', 60);
    console.log(game);
}
