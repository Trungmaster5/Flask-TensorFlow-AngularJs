import glob
import os
import librosa
import numpy as np
import tensorflow as tf
from sklearn.metrics import precision_recall_fscore_support
from flask import Flask, jsonify, render_template, request

###DEFINE FUNCTION #####
def extract_feature(file_name):
    X, sample_rate = librosa.load(file_name)
    stft = np.abs(librosa.stft(X))
    mfccs = np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=40).T,axis=0)
    chroma = np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T,axis=0)
    mel = np.mean(librosa.feature.melspectrogram(X, sr=sample_rate).T,axis=0)
    contrast = np.mean(librosa.feature.spectral_contrast(S=stft, sr=sample_rate).T,axis=0)
    tonnetz = np.mean(librosa.feature.tonnetz(y=librosa.effects.harmonic(X), sr=sample_rate).T,axis=0)
    return mfccs,chroma,mel,contrast,tonnetz

def parse_audio_files(parent_dir,sub_dirs,file_ext='*.wav'):
    features, labels = np.empty((0,193)), np.empty(0)
    for label, sub_dir in enumerate(sub_dirs):
        for fn in glob.glob(os.path.join(parent_dir, sub_dir, file_ext)):
            mfccs, chroma, mel, contrast,tonnetz = extract_feature(fn)
            ext_features = np.hstack([mfccs,chroma,mel,contrast,tonnetz])
            features = np.vstack([features,ext_features])
            labels = np.append(labels, fn.split('/')[3].split('-')[1])
            ## Move to the third '/' of source url then get the character after first '-'
            ## E.g. UrbanSound8K/audio/fold1/7061-6-0-0.wav
            ## Label = 6
    return np.array(features), np.array(labels, dtype = np.int)

def parse_audio_file_for_prediction(parent_dir,file_ext='*.wav'):
    features, labels = np.empty((0,193)), np.empty(0)
    for fn in glob.glob(os.path.join(parent_dir,file_ext)):
        mfccs, chroma, mel, contrast,tonnetz = extract_feature(fn)
        ext_features = np.hstack([mfccs,chroma,mel,contrast,tonnetz])
        features = np.vstack([features,ext_features])
        labels = np.append(labels, fn.split('/')[3].split('-')[1])
        ## Move to the first'/' of source url then get the character after first '-'
        ## E.g. UrbanSound8K/audio/fold1/7061-6-0-0.wav
        ## Label = 6
    return np.array(features), np.array(labels, dtype = np.int)

def one_hot_encode(labels):
    n_labels = len(labels)
    n_unique_labels = len(np.unique(labels))
    one_hot_encode = np.zeros((n_labels,n_unique_labels))
    one_hot_encode[np.arange(n_labels), labels] = 1
    return one_hot_encode

# webapp
app = Flask(__name__)

@app.route('/api/predict',methods=['POST'])
def predict():
	content = request.get_json()
	value = content.get('media')
	print content, value
	with tf.Session() as sess:
	    ### LOAD PRESAVED MODEL ###
	    saver = tf.train.import_meta_graph('./model/trained_model-2000.meta')
	    saver.restore(sess,tf.train.latest_checkpoint('./model'))
	    print ('MODEL LOADED !')
	    #sess.run(tf.global_variables_initializer())

	    ### GET FEEDDATA###
	    #parent_dir = 'media'
	    parent_dir='static/media/'+value
	    get_features, get_labels = parse_audio_file_for_prediction(parent_dir)
	    #print get_features

	    graph = tf.get_default_graph()
	    operator = graph.get_tensor_by_name("operator:0")
	    X = graph.get_tensor_by_name("X:0")
	    #print X

	    y_pred= sess.run(tf.argmax(operator,1), feed_dict={X:get_features})
	    confidence= np.amax(sess.run(operator, feed_dict={X:get_features}))
	    print 'PREDICTION:', y_pred
	    print 'CONFIDENCE:', confidence
	    print 'REAL VALUE:', get_labels
	return jsonify(predict=np.asscalar(y_pred), confidence=np.asscalar(confidence), true_labels=np.asscalar(get_labels))


@app.route('/')
def main():
	return render_template('index.html')

if __name__ == "__main__":
    app.run()
