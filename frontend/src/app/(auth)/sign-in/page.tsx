"use client";

import { useRouter } from "next/navigation";
import { FormEvent, useState } from "react";

const page = () => {
  const [email, setEmail] = useState<string>("");
  const [password, setPassword] = useState<string>("");

  const [loading, setLoading] = useState<boolean>(false);
  const [message, setMessage] = useState<string>("");

  const router = useRouter();

  const handleLogin = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    setLoading(true);
    setMessage("");

    try {
      const response = await fetch("http://localhost:8000/auth/login", {
        method: "POST",

        headers: {
          "Content-Type": "application/json",
        },

        body: JSON.stringify({
          email,
          password,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        localStorage.setItem("token", data.access_token);
        setMessage("Login successful");
        router.push("/dashboard");
      } else {
        setMessage(data.message || "Login failed");
      }
    } catch (error) {
      setMessage("Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main
      className="
        min-h-screen
        flex
        items-center
        justify-center
        bg-white
        px-4
      "
    >
      <div
        className="
          w-full
          max-w-sm
          border
          border-gray-200
          rounded-2xl
          p-8
          bg-white
        "
      >
        <h1
          className="
            text-2xl
            font-semibold
            text-black
            text-center
          "
        >
          Welcome Back
        </h1>

        <p
          className="
            text-sm
            text-gray-500
            text-center
            mt-2
          "
        >
          Login to your account
        </p>

        <form
          onSubmit={handleLogin}
          className="
            mt-8
            space-y-5
          "
        >
          {/* Email */}

          <div>
            <label
              className="
                text-sm
                font-medium
                text-black
              "
            >
              Email
            </label>

            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="you@example.com"
              required
              className="
                mt-2
                w-full
                px-4
                py-3
                rounded-xl
                border
                border-gray-300
                bg-white
                text-black
                placeholder:text-gray-400
                outline-none
                transition

                focus:border-black
                focus:ring-1
                focus:ring-black
              "
            />
          </div>

          {/* Password */}

          <div>
            <label
              className="
                text-sm
                font-medium
                text-black
              "
            >
              Password
            </label>

            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="********"
              required
              className="
                mt-2
                w-full
                px-4
                py-3
                rounded-xl
                border
                border-gray-300
                bg-white
                text-black
                placeholder:text-gray-400
                outline-none
                transition

                focus:border-black
                focus:ring-1
                focus:ring-black
              "
            />
          </div>

          {/* Button */}

          <button
            type="submit"
            disabled={loading}
            className="
              w-full
              py-3
              rounded-xl
              bg-black
              text-white
              font-medium
              transition

              hover:bg-gray-800

              disabled:opacity-50
            "
          >
            {loading ? "Logging in..." : "Login"}
          </button>

          {/* Message */}

          {message && (
            <p
              className={`
                  text-center
                  text-sm
                  font-medium

                  ${
                    message.includes("successful")
                      ? "text-black"
                      : "text-gray-500"
                  }
                `}
            >
              {message}
            </p>
          )}
        </form>
      </div>
    </main>
  );
};

export default page;
