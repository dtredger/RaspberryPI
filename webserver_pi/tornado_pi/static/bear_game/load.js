var load_state = {

	// static_file_location = "/static/bear_game/assets/"
	// Function called first to load all the assets
	preload: function() {
		this.game.stage.backgroundColor = '#ffffff';
		this.game.load.image('bear', '/static/bear_game/assets/bear.png');
		this.game.load.image('pipe', '/static/bear_game/assets/pipe.png');
		this.game.load.image('lemongrab', '/static/bear_game/assets/lemongrab.png')

		this.game.load.audio('jump', '/static/bear_game/assets/jump.wav');
		this.game.load.audio('unacceptable', '/static/bear_game/assets/unacceptable.wav');
	},

	// Fuction called after 'preload' to setup the game
	create: function() { 

		// go to game menu
		this.game.state.start('menu');
	}


};
