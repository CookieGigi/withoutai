import "@copilotkit/react-core/v2/styles.css";
import { CopilotProvider } from "./components/copilot_provider";

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <CopilotProvider>{children}</CopilotProvider>
      </body>
    </html>
  );
}
