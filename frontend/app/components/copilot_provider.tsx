"use client";
import { CopilotKit } from "@copilotkit/react-core/v2";
import { createContext, useState } from "react";

export const ModelContext = createContext<{
  model: string | undefined;
  set_model: (m: string | undefined) => void;
}>({ model: undefined, set_model: () => {} });

export function CopilotProvider({ children }: { children: React.ReactNode }) {
  const [model, set_model] = useState<string | undefined>(undefined);
  return (
    <CopilotKit
      runtimeUrl="/api/copilotkit"
      agent="simple"
      properties={{ model }}
    >
      <ModelContext.Provider value={{ model, set_model: set_model }}>
        {children}
      </ModelContext.Provider>
    </CopilotKit>
  );
}
