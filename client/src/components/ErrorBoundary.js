import React from "react";

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null, errorInfo: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    this.setState({
      error,
      errorInfo,
    });
    // Log error to console in development
    if (process.env.NODE_ENV === "development") {
      console.error("Error caught by boundary:", error, errorInfo);
    }
  }

  handleReset = () => {
    this.setState({ hasError: false, error: null, errorInfo: null });
  };

  render() {
    if (this.state.hasError) {
      return (
        <div className="error-boundary" style={{
          padding: "2rem",
          textAlign: "center",
          color: "var(--text-color)",
          background: "var(--surface-color)",
          borderRadius: "8px",
          border: "1px solid var(--border-color)",
          margin: "2rem auto",
          maxWidth: "600px"
        }}>
          <h2>⚠️ משהו השתבש</h2>
          <p>אנא רענן את הדף או נסה שוב מאוחר יותר.</p>
          {process.env.NODE_ENV === "development" && this.state.error && (
            <details style={{ marginTop: "1rem", textAlign: "left" }}>
              <summary style={{ cursor: "pointer", marginBottom: "0.5rem" }}>
                פרטי שגיאה (פיתוח בלבד)
              </summary>
              <pre style={{
                background: "#1a1a1a",
                padding: "1rem",
                borderRadius: "4px",
                overflow: "auto",
                fontSize: "12px"
              }}>
                {this.state.error.toString()}
                {this.state.errorInfo?.componentStack}
              </pre>
            </details>
          )}
          <button
            onClick={this.handleReset}
            style={{
              marginTop: "1rem",
              padding: "10px 20px",
              background: "var(--accent)",
              color: "#121212",
              border: "none",
              borderRadius: "4px",
              cursor: "pointer",
              fontSize: "16px"
            }}
          >
            נסה שוב
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
