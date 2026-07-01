"use client";

import { useContext, useEffect, useState } from "react";
import { ModelContext } from "./copilot_provider";

type ModelInfo = {
  id: string;
  name: string;
  can_think: boolean;
  can_vision: boolean;
  max_tokens: number | null;
  max_input_tokens: number | null;
  max_output_tokens: number | null;
  input_cost_per_token: number | null;
  output_cost_per_token: number | null;
  provider: string;
  mode: string;
  can_function_call: boolean;
  can_tool_choice: boolean;
  can_prompt_cache: boolean;
};

export default function ModelSelector() {
  const { model, set_model } = useContext(ModelContext);
  const [models, set_models] = useState<ModelInfo[]>([]);
  const [loading, set_loading] = useState(true);
  const [error, set_error] = useState<string | null>(null);

  useEffect(() => {
    Promise.all([
      fetch("/models").then((r) => {
        if (!r.ok) throw new Error(`list HTTP ${r.status}`);
        return r.json() as Promise<ModelInfo[]>;
      }),
      fetch("/models/current").then((r) => {
        if (!r.ok) throw new Error(`current HTTP ${r.status}`);
        return r.json() as Promise<string>;
      }),
    ])
      .then(([list, current]) => {
        set_models(list);
        set_model(current ?? list[0]); // seed default
      })
      .catch((e) => set_error(String(e)))
      .finally(() => set_loading(false));
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  if (loading) return <p>loading models…</p>;
  if (error) return <p>error: {error}</p>;

  return (
    <select
      value={model ?? ""}
      onChange={(e) => set_model(e.target.value || undefined)}
    >
      {models.map((m) => (
        <option key={m.id} value={m.id}>
          {m.name}
        </option>
      ))}
    </select>
  );
}
