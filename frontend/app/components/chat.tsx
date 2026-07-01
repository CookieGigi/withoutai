"use client";

import {
  CopilotChat,
  useConfigureSuggestions,
} from "@copilotkit/react-core/v2";
import ModelSelector from "./models_selector";

export default function Chat() {
  useConfigureSuggestions({
    suggestions: [
      { title: "Write a sonnet", message: "Write a short sonnet about AI." },
      {
        title: "Tell me a joke",
        message: "Tell me a one-line joke.",
      },
      {
        title: "Is 17 prime?",
        message: "Walk me through whether 17 is prime.",
      },
    ],
    available: "always",
  });
  return <CopilotChat attachments={{ enabled: true }} />;
}
