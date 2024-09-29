import { useState } from 'react';

const NEXT_PUBLIC_API_BASE_URL="http://127.0.0.1:5000"

export default function Home() {
  const [disease, setDisease] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSearch = async () => {
    setLoading(true);
    setError(null);
    setResults([]);

    // Construct the query parameters
    const params = new URLSearchParams();
    if (disease.trim() !== '') {
      params.append('disease', disease.trim());
    }

    try {
      const response = await fetch(
        `${NEXT_PUBLIC_API_BASE_URL}/search?${params.toString()}`
      );

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      setResults(data);
    } catch (err) {
      setError('Failed to fetch data. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.container}>
      <h1>Clinical Trials Search</h1>
      <div style={styles.form}>
        <div style={styles.inputGroup}>
          <label htmlFor="disease">Disease:</label>
          <input
            type="text"
            id="disease"
            value={disease}
            onChange={(e) => setDisease(e.target.value)}
            placeholder="e.g., NSCLC"
            style={styles.input}
          />
        </div>
        <button onClick={handleSearch} style={styles.button} disabled={loading}>
          {loading ? 'Searching...' : 'Search'}
        </button>
      </div>

      {error && <p style={styles.error}>{error}</p>}

      <h2>Results:</h2>
      {results.length === 0 && !loading && <p>No trials found.</p>}
      <ul style={styles.list}>
        {results.map((title, index) => (
          <li key={index} style={styles.listItem}>
            {title}
          </li>
        ))}
      </ul>
    </div>
  );
}

const styles = {
  container: {
    maxWidth: '600px',
    margin: '50px auto',
    padding: '0 20px',
    fontFamily: 'Arial, sans-serif',
  },
  form: {
    marginBottom: '20px',
    padding: '20px',
    border: '1px solid #ccc',
    borderRadius: '5px',
  },
  inputGroup: {
    marginBottom: '15px',
  },
  input: {
    width: '100%',
    padding: '8px',
    marginTop: '5px',
    boxSizing: 'border-box',
  },
  button: {
    padding: '10px 15px',
    backgroundColor: '#0070f3',
    color: '#fff',
    border: 'none',
    borderRadius: '5px',
    cursor: 'pointer',
  },
  list: {
    listStyleType: 'disc',
    paddingLeft: '20px',
  },
  listItem: {
    marginBottom: '10px',
  },
  error: {
    color: 'red',
  },
};
