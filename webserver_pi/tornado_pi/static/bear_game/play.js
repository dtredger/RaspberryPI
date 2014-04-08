var play_state = {

	create: function() {
		var space_key = this.game.input.keyboard.addKey(Phaser.Keyboard.SPACEBAR);
		space_key.onDown.add(this.jump, this);

		// pipes
		this.pipes = game.add.group();
		this.pipes.createMultiple(20, 'pipe');
		this.timer = this.game.time.events.loop(1500, this.add_row_of_pipes, this);	

		// bear
		this.bear = this.game.add.sprite(100, 245, 'bear');
		this.bear.body.gravity.y = 1000;
		this.bear.anchor.setTo(-0.2, 0.5);

		// sound
		this.jump_sound = this.game.add.audio('jump');
		this.gameover_sound = this.game.add.audio('unacceptable');

		// score
		score = 0;
		var style = { font: "30px Arial", fill: "00000f" };
		this.label_score = this.game.add.text(20, 20, "0", style); 		
	},

	update: function() {
		if (this.bear.inWorld == false) {
			setTimeout(function() {
				play_state.restart_game()
			}, 2000);
		}
		if (this.bear.angle < 20) {
			this.bear.angle += 1;
		}
		this.game.physics.overlap(this.bear, this.pipes, this.hit_pipe, null, this);
	},

	// --- custom functions --- //

	add_one_pipe: function(x, y) {
		var pipe = this.pipes.getFirstDead();
		pipe.reset(x, y);

		pipe.body.velocity.x = -200;
		pipe.outOfBoundsKill = true;
	},

	add_row_of_pipes: function() {
		var hole = Math.floor(Math.random()*5) + 1;
		for (var i = 0; i < 8; i++) {
			if (i != hole && i != hole +1) {
				this.add_one_pipe(400, i*60 + 10);
			}
		}
		score += 1;
		this.label_score.content = score;
	},

	jump: function() {
		if (this.bear.alive == false) {
			return;
		}
		this.bear.body.velocity.y = -200;

		var animation = this.game.add.tween(this.bear);
		animation.to({angle:-20}, 100)
		animation.start();

		this.jump_sound.play();
	},

	hit_pipe: function() {
		if (this.bear.alive == false) {
			return;
		}
		this.bear.alive = false;
		this.game.time.events.remove(this.timer);
		this.pipes.forEachAlive(function(p) {
			p.body.velocity.x = 0;
		}, this);
		this.lose_screen = this.game.add.sprite(0,0, 'lemongrab');
		setTimeout(function() {
			play_state.gameover_sound.play()
		}, 2000);
		
	},

	restart_game: function() {
		// this.game.time.events.remove(this.timer);

		this.game.state.start('menu');
	}

};