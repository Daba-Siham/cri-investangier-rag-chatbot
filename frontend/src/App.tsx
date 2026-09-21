import { ChatWidget } from "./components/ChatWidget";
import { useChat } from "./hooks/useChat";

export default function App() {
  const chat = useChat();
  return <ChatWidget messages={chat.messages} loading={chat.loading} error={chat.error} serviceStatus={chat.serviceStatus} onSend={chat.send} onNewConversation={() => void chat.newConversation()} />;
}
