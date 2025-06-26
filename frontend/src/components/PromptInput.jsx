import React, { useState } from 'react';
import { generateVideo } from '../services/api';

function PromptInput() {
  const [prompt, setPrompt] = useState('');
  const [videoUrl, setVideoUrl] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    if (!prompt.trim()) return;

    setLoading(true);
    setVideoUrl('');
    setError('');

    try {
      const res = await generateVideo(prompt);
      const filename = res.video_path.split('/').pop();

      if (res.status === 'success') {
        setVideoUrl(`http://localhost:8000/api/videos/${filename}`);
      } else {
        setError(res.message || 'Unknown error occurred.');
      }
    } catch (err) {
      console.error(err);
      setError('Error contacting backend. Please try again.');
    }

    setLoading(false);
  };

  return (
    <div style={styles.container}>
      <h2 style={styles.title}>🎬 Manim Video Generator</h2>

      <textarea
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        placeholder="Describe the scene you want..."
        rows={6}
        disabled={loading}
        style={styles.textarea}
      />

      <button
        onClick={handleSubmit}
        disabled={loading || !prompt.trim()}
        style={styles.button}
      >
        {loading ? 'Generating...' : 'Generate'}
      </button>

      {error && <div style={styles.error}>{error}</div>}

      {videoUrl && (
        <div style={styles.videoContainer}>
          <h4>Generated Video:</h4>
          <video src={videoUrl} controls style={styles.video} />
        </div>
      )}
    </div>
  );
}

const styles = {
  container: {
    maxWidth: '700px',
    margin: '40px auto',
    padding: '20px',
    border: '1px solid #ddd',
    borderRadius: '12px',
    backgroundColor: '#f9f9f9',
    fontFamily: 'Arial, sans-serif',
  },
  title: {
    textAlign: 'center',
    marginBottom: '20px',
  },
  textarea: {
    width: '100%',
    padding: '12px',
    fontSize: '16px',
    borderRadius: '8px',
    border: '1px solid #ccc',
    resize: 'vertical',
    marginBottom: '10px',
  },
  button: {
    padding: '10px 20px',
    fontSize: '16px',
    backgroundColor: '#4CAF50',
    color: 'white',
    border: 'none',
    borderRadius: '6px',
    cursor: 'pointer',
  },
  error: {
    marginTop: '15px',
    color: 'red',
    textAlign: 'center',
  },
  videoContainer: {
    marginTop: '20px',
    textAlign: 'center',
  },
  video: {
    width: '100%',
    maxHeight: '400px',
    borderRadius: '8px',
    background: 'black',
  },
};

export default PromptInput;
