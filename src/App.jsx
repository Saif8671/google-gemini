import React, { useState, useRef } from 'react';
import { useDropzone } from 'react-dropzone';
import ReactMarkdown from 'react-markdown';
import { GoogleGenerativeAI } from '@google/generative-ai';

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [agendaText, setAgendaText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const chatEndRef = useRef(null);

  const genAI = new GoogleGenerativeAI('AIzaSyBQMv2YdwHydWYNr1vBHJNIggXP61v3-Vc');

  const { getRootProps, getInputProps } = useDropzone({
    accept: {
      'application/pdf': ['.pdf'],
    },
    onDrop: async (acceptedFiles) => {
      const file = acceptedFiles[0];
      if (file) {
        const arrayBuffer = await file.arrayBuffer();
        const pdfParser = await import('pdf-parse');
        const data = await pdfParser.default(Buffer.from(arrayBuffer));
        setAgendaText(data.text);
      }
    },
  });

  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim() || !agendaText) return;

    const userMessage = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const model = genAI.getGenerativeModel({ model: 'gemini-pro' });
      const prompt = `Event information: ${agendaText}\n\nQuestion: ${input}\n\nYou are a friendly Event Information Assistant. Answer the question based on the event information provided. If the information is not available, politely say so.`;
      
      const result = await model.generateContent(prompt);
      const response = await result.response;
      const botMessage = { role: 'assistant', content: response.text() };
      
      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('Error:', error);
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: 'Sorry, I encountered an error. Please try again.' 
      }]);
    }

    setIsLoading(false);
    scrollToBottom();
  };

  return (
    <div className="min-h-screen bg-gray-100 p-4">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold text-center mb-8">
          🤖 GuiderStartBot - Your Event Companion
        </h1>

        <div className="bg-white rounded-lg shadow-md p-4 mb-8">
          <div {...getRootProps()} className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center">
            <input {...getInputProps()} />
            <p>Drag & drop an agenda PDF here, or click to select one</p>
          </div>
          {agendaText && (
            <div className="mt-4">
              <h3 className="font-semibold mb-2">Agenda Preview:</h3>
              <div className="bg-gray-50 p-4 rounded max-h-40 overflow-y-auto">
                <pre className="whitespace-pre-wrap">{agendaText.substring(0, 500)}...</pre>
              </div>
            </div>
          )}
        </div>

        <div className="bg-white rounded-lg shadow-md p-4">
          <div className="h-96 overflow-y-auto mb-4">
            {messages.map((message, index) => (
              <div
                key={index}
                className={`mb-4 ${
                  message.role === 'user' ? 'text-right' : 'text-left'
                }`}
              >
                <div
                  className={`inline-block p-3 rounded-lg ${
                    message.role === 'user'
                      ? 'bg-blue-500 text-white'
                      : 'bg-gray-200 text-gray-800'
                  }`}
                >
                  <ReactMarkdown>{message.content}</ReactMarkdown>
                </div>
              </div>
            ))}
            {isLoading && (
              <div className="text-center text-gray-500">
                Bot is thinking...
              </div>
            )}
            <div ref={chatEndRef} />
          </div>

          <form onSubmit={handleSubmit} className="flex gap-2">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask about the event..."
              className="flex-1 p-2 border rounded"
              disabled={!agendaText || isLoading}
            />
            <button
              type="submit"
              disabled={!agendaText || isLoading}
              className="bg-blue-500 text-white px-4 py-2 rounded disabled:bg-gray-300"
            >
              Send
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}

export default App;