require('dotenv').config();
const axios = require('axios');

const OPENAI_API_KEY = process.env.OPENAI_API_KEY;
const AIDEVS_KEY = process.env.AIDEVS_KEY;

if (!OPENAI_API_KEY || !AIDEVS_KEY) {
  console.error("Missing keys in .env 😤");
  process.exit(1);
}

async function processWithGPT4(description) {
  try {
    const response = await axios.post(
      'https://api.openai.com/v1/chat/completions',
      {
        model: "gpt-4",
        messages: [
          {
            role: "system",
            content: "You are a helpful assistant that transforms imprecise or technical robot descriptions into detailed visual descriptions for image generation models like DALL·E. Your goal is to describe the robot in the most visual and concrete way possible. Include its external appearance, size, color, material type, facial expression (if any), limb type, power source, or other characteristic elements. Avoid describing the robot's operation - focus solely on its physical appearance. The response must be in English only."
          },
          {
            role: "user",
            content: description
          }
        ]
      },
      {
        headers: {
          'Authorization': `Bearer ${OPENAI_API_KEY}`,
          'Content-Type': 'application/json'
        }
      }
    );
    return response.data.choices[0].message.content;
  } catch (error) {
    if (error.message) {
      console.error("❌ Error processing with GPT-4:", error.message);
    }
    throw error;
  }
}

async function generateImage(prompt) {
  try {
    const response = await axios.post(
      'https://api.openai.com/v1/images/generations',
      {
        model: 'dall-e-3',
        prompt: prompt,
        n: 1,
        size: "1024x1024"
      },
      {
        headers: {
          'Authorization': `Bearer ${OPENAI_API_KEY}`,
          'Content-Type': 'application/json'
        }
      }
    );
    return response.data.data[0].url;
  } catch (error) {
    console.error("❌ Error generating image:", error.message);
    throw error;
  }
}

async function submitAnswer(imageUrl) {
  try {
    const response = await axios.post(
      'https://c3ntrala.ag3nts.org/report',
      {
        task: "robotid",
        apikey: AIDEVS_KEY,
        answer: imageUrl
      }
    );
    console.log("✅ Answer submitted successfully:", response.data);
    return response.data;
  } catch (error) {
    console.error("❌ Error submitting answer:", error.message);
    throw error;
  }
}

async function fetchRobotData() {
  try {
    const url = `https://c3ntrala.ag3nts.org/data/${AIDEVS_KEY}/robotid.json`;
    const response = await axios.get(url);
    const robotData = response.data;

    console.log("🤖 Original robot description:", robotData);
    
    // Convert robotData to string if it's an object
    const descriptionString = typeof robotData === 'object' ? JSON.stringify(robotData) : robotData;
    
    // Process description with GPT-4
    const processedDescription = await processWithGPT4(descriptionString);
    console.log("📝 Processed description:", processedDescription);
    
    // Generate image based on processed description
    const imageUrl = await generateImage(processedDescription);
    console.log("🎨 Generated image URL:", imageUrl);
    
    // Submit the answer
    await submitAnswer(imageUrl);
    
    return { robotData, processedDescription, imageUrl };
  } catch (error) {
    console.error("❌ Error while fetching robot data:", error.message);
  }
}

fetchRobotData();
