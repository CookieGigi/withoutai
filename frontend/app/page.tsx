import Chat from "./components/chat";
import ModelSelector from "./components/models_selector";

export default function Page() {
  return (
    <main>
      <ModelSelector />
      <Chat />
    </main>
  );
}
