// LIVE ASSIGNER
// MATTHEW STEIN - SPRING 2014

(
a = (); //assigned dictionary
m = []; //sortedMIDI

~playAssign = { |notes|

	~insertInPlace = { |elt|
		var length = m.size;
		if((length==0), {m.add(elt)},
			{
				var i=0, done = false;
				while({(i < length) && (done==false)},
					{ if(elt < m[i],
						{done = true},
						{i = i+1}
						);
				});
				m = m.insert(i, elt);
		});
	};

	SynthDef("Whizbang", { | freq, bufnum, sustain = 1, thresh = 0.05, in = 1 |
		var trig, trg, amp, input, trgReply;
		Out.ar(0, Linen.kr(Trig1.kr(1, sustain)) * SinOsc.ar(freq));
		trig = 1 - Trig1.kr(1, 2);

		amp = Amplitude.ar(Mix.ar(SoundIn.ar(0))) > thresh;
		trg = Trig1.kr(amp * trig, 3);

		input = AudioIn.ar(in);

		RecordBuf.ar(input, bufnum,
			loop:0,
			trigger:trg,
			doneAction:2);

		trgReply = Slope.kr(trg) < 0;
		SendReply.kr (trgReply, '/recorded');
	}).add;

	~notes = Pseq(notes).asStream;

	f = {
		var buffer, n = ~notes.next;
		if (n.notNil) {
			Routine({
				var buf = Buffer.alloc(s, 3 * 44100);
				a[n] = buf;
				~insertInPlace.(n);
				s.sync;
				Synth("Whizbang", [bufnum: buf, freq: n.midicps ]);

			}).next;
		};
	};

	OSCdef(\tt, f, '/recorded');
	f.value;

};
)

(
~findClosest = { | val, arr |
	case
	{ size(arr) == 1} { arr[0] }
	{ val < arr[0] } { arr[0]}
	{ val > arr[0] && val < arr[1] } {if ((val-arr[0])<(arr[1]-val), {arr[0]}, {arr[1]})}
	{ val > arr[1] } { ~findClosest.(val, arr.copyRange(1, arr.size-1)) };
};


~interactMode = {

	Server.default.waitForBoot {
		b = Buffer.alloc(s, 512).postln;
		s.sync;

		SynthDef("listener", {
			var sig, chain, freq, hasFreq, onsets;
			sig = SoundIn.ar(0);
			chain = FFT(b, sig);
			# freq, hasFreq = Tartini.kr(sig);
			onsets = Onsets.kr(chain, 0.5).poll;
			SendReply.kr(onsets * hasFreq, '/newNote', [freq]);
		}).add;

		SynthDef("response", { |bufnum|
			Out.ar(0, PlayBuf.ar(1, bufnum, doneAction:2));
		}).add;

		s.sync;

		f = {
			var startTime = 0;
			{ |msg, time |
				var freq = msg.asArray[3], closest, buf;
				msg.postln;
				if ((time - startTime) > 0.1) {
					closest = ~findClosest.(freq.cpsmidi, m);
					buf = a[closest];
					Synth("response", [\bufnum, buf]);
				};
				startTime = time;
				msg.postln;

			};
		}.value;

		OSCdef(\uu, f, '/newNote');
		Synth("listener");
		f.value(nil,0) ;
	};
};

)

~playAssign.([62,69,70]);
~interactMode.value;