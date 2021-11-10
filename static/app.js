
class BoggleGame{

    constructor(container, time){
        this.board = $(container);
        this.time = time;
        this.score = 0;
        this.words = new Set();
    }

    //method to collect and send word to server for check...also displays result
    async checkWord(e){
        e.preventDefault();
    
        //collect the word guessed entered in the form input
        const guess = $('#guess', this.board).val();
        $('#guess', this.board).val('');
        //send request to server for checking the word guessed in the form
        if (guess){
            const res = await axios.get("/word", {params:{word:guess}});
            const result = res.data.result;
            //display results
            if(!this.words.has(guess)){
                if (result === "not-word") {
                    this.message(`${guess} is not a valid word`, "error")
                } else if (res.data.result === "not-on-board") {
                    this.message(`${guess} is not on the board`, "error");
                } else {
                    this.showWord(guess);
                    this.message(`Scored: ${guess}`, "good"); 
                    this.computeScore(guess);
                    this.words.add(guess);
                }
            } else{
                this.message(`${guess} already found...try again`, "error")
            }
        } else{
            this.message('Enter a word...','error');

        }
    }

    //method to show the word
    showWord(word){
            const $list = $('#wordList', this.board);
            $list.append(`<li>${word}</li>`)
    }

    //method to show a result message
    message(result, type){
        const $message = $('.message', this.board);
        $message.text(result).addClass(type);
    }

     //method to shandle scoring
    computeScore(word){
        this.score += word.length;
        const $score = $('.score', this.board);
        $score.text(`Score: ${this.score}`);
    }

    //show time
    showTime(){
         this.time -= 1 ;
         const $time = $('.timer', this.board);
         $time.text(`Time (s): ${this.time}`);
    }

    //Final score handle (end of game)
    async endGame(e) {
        e.preventDefault();
        $(".table", this.board).hide();
        $(".list", this.board).hide();

        const res = await axios.post("/end", {finalScore:this.score});
        let sessionScore = res.data.record
        let sessionPlays = res.data.plays
        this.message(`Record for the session: ${sessionScore} / Number of plays: ${sessionPlays}`, "good");
    }
}
 
//create game instance only when board page is loaded
if ($('.boardPage').length){
    let game = new BoggleGame('.boardPage', 60);
    $('#guessSubmit').on("click", game.checkWord.bind(game));
    $('#refresh').on("click", function(e){
        e.preventDefault();
        location.reload();
    });
     $('#end').on("click", game.endGame.bind(game));

    //setup and stop timer
    let timer = setInterval(game.showTime.bind(game), 1000);
    setTimeout(clearInterval, 60000, timer);
    setTimeout(function(){
        $('#guessSubmit').prop('disabled', true).addClass('off');
    }, 60500);
    
    //end of game
    setTimeout(function(){
        $('#end').prop('disabled', false).removeClass('off');
    }, 60500);
}
