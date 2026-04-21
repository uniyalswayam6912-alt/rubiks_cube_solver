export async function fetchSolution(moves) {
  try {
    const response = await fetch("http://127.0.0.1:8000/solve", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ moves }),
    });

    if (!response.ok) {
      throw new Error(`Server error: ${response.status}`);
    }

    const data = await response.json();
    if (data.error) {
      throw new Error(data.error);
    }
    return data;
  } catch (error) {
    console.error("API Fetch Error:", error);
    throw error;
  }
}
