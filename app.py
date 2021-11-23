from flask import Flask, request, render_template, Response
from audio import recognize_audio
from video import gen_frames
from fuzzywuzzy import fuzz 
import re
from data import *


def compare_texts(target):
    #target = re.sub('[^А-Яа-я]', ' ', target)
    text_out = recognize_audio()
    score = fuzz.ratio(text_out.lower(), target.lower())

    return text_out, score


app = Flask(__name__)
        

@app.route('/')
def start():
    return render_template('start.html')


@app.route('/text', methods=['GET', 'POST'])
def text_from_text():
    if request.method == 'GET':
        return render_template('text.html')

    else:
        if request.form['submit_button'] == 'Распознать по голосу':
            curr_sent = request.form['text']
            text_out, score = compare_texts(curr_sent)
            
            return render_template('text.html',
                                    sentence=curr_sent,
                                    number=True,
                                    audio=True,
                                    text_out=text_out,
                                    score=score)

        elif request.form['submit_button'] == 'Распознать по лицу':
            curr_sent = request.form['text']
            return render_template('text.html',
                                    sentence=curr_sent,
                                    number=True,
                                    video=True)


        elif request.form['submit_button'] == 'Остановить видео':
            curr_sent = request.form['text']
            return render_template('text.html',
                                    sentence=curr_sent,
                                    number=True,
                                    stop_video=True)

        else:
            curr_sent = sentences[int(request.form['submit_button'])-1]
            return render_template('text.html',
                                    sentence=curr_sent,
                                    number=True)


@app.route('/audio', methods=['GET', 'POST'])
def text_from_audio():

    if request.method == 'GET':
        return render_template('audio.html')

    else:
        if request.form['submit_button'] == 'Распознать по голосу':
            curr_audio = request.form['audio']
            curr_text = request.form['text']

            text_out, score = compare_texts(curr_text)
            
            return render_template('audio.html',
                                    number=True,
                                    audio=True,
                                    curr_audio=curr_audio,
                                    curr_text=curr_text,
                                    text_out=text_out,
                                    score=score)

        elif request.form['submit_button'] == 'Распознать по лицу':
            curr_audio = request.form['audio']
            curr_text = request.form['text']
            return render_template('audio.html',
                                    curr_audio=curr_audio,
                                    curr_text=curr_text,
                                    number=True,
                                    video=True
                                    )

        elif request.form['submit_button'] == 'Остановить видео':
            curr_audio = request.form['audio']
            curr_text = request.form['text']
            return render_template('audio.html',
                                    curr_audio=curr_audio,
                                    curr_text=curr_text,
                                    number=True,
                                    stop_video=True
                                    )

        else:
            curr_audio = list(sounds.keys())[int(request.form['submit_button'])-1]
            curr_text = list(sounds.values())[int(request.form['submit_button'])-1]
            return render_template('audio.html',
                                    curr_audio=curr_audio,
                                    curr_text=curr_text,
                                    number=True)


@app.route('/video', methods=['GET', 'POST'])
def text_from_video():

    if request.method == 'GET':
        return render_template('video.html')

    else:
        if request.form['submit_button'] == 'Распознать по голосу':
            curr_video = request.form['video']
            curr_text = request.form['text']

            text_out, score = compare_texts(curr_text)
            
            return render_template('video.html',
                                    number=True,
                                    audio=True,
                                    text_out=text_out,
                                    curr_video=curr_video,
                                    curr_text=curr_text,
                                    score=score)


        elif request.form['submit_button'] == 'Распознать по лицу':
            curr_video = request.form['video']
            curr_text = request.form['text']
            return render_template('video.html',
                                    curr_video=curr_video,
                                    curr_text=curr_text,
                                    number=True,
                                    video=True)

        elif request.form['submit_button'] == 'Остановить видео':
            curr_video = request.form['video']
            curr_text = request.form['text']
            return render_template('video.html',
                                    curr_video=curr_video,
                                    curr_text=curr_text,
                                    number=True,
                                    stop_video=True)

        else:
            curr_video = list(videos.keys())[int(request.form['submit_button'])-1]
            curr_text = list(videos.values())[int(request.form['submit_button'])-1]
            return render_template('video.html',
                                    curr_video=curr_video,
                                    curr_text=curr_text,
                                    number=True)


@app.route('/video_feed', methods=['GET', 'POST'])
def video_feed():
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')



if __name__ == "__main__":
    app.run(debug=False, port=1234)#, host='0.0.0.0')
