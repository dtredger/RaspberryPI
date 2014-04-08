var menu_state = {

	create: function() {

		// spacebar to jump
		var space_key = this.game.input.keyboard.addKey(Phaser.Keyboard.SPACEBAR);
		space_key.onDown.add(this.start, this);

		// menu style
		var style = {
			font: "30px Arial", 
			fill: "00000f"
		};
		var x = game.world.width/2;
		var y = game.world.height/2;

		var text = this.game.add.text(x, y-50, "Press space to start", style);
		text.anchor.setTo(0.5, 0.5);

		if (score > 0) {
			var score_label = this.game.add.text(x, y+50, "last score: " + score, style);
			score_label.anchor.setTo(0.5, 0.5);
		}
	},

	start: function() {
		this.game.state.start('play');
	}
};