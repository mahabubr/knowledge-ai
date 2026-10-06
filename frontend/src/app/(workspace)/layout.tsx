"use client";

import { useRouter } from "next/navigation";
import { useEffect } from "react";

interface IProps {
  children: React.ReactNode;
}

const layout = ({ children }: IProps) => {
  const router = useRouter();

  useEffect(() => {
    const token = localStorage.getItem("token");

    if (!token) {
      router.push("/sign-in");
    }
  }, []);

  return <div className="p-10">{children}</div>;
};

export default layout;
