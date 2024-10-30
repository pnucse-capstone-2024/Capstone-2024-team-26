"use client";

import React, { useState } from "react";
import { Dialog, DialogTrigger, DialogContent } from "../components/ui/dialog";
import { Input } from "../components/ui/input";
import { Label } from "../components/ui/label";
import { Select, SelectTrigger, SelectContent, SelectItem } from "../components/ui/select";
import { Button } from "../components/ui/button";
import MainPage from "./MainPage";

const ModalFlow = () => {
  const [showFirstModal, setShowFirstModal] = useState(false);
  const [showSecondModal, setShowSecondModal] = useState(false);
  const [name, setName] = useState("");
  const [gender, setGender] = useState("");

  const handleNext = () => {
    setShowFirstModal(false);
    setShowSecondModal(true);
  };

  const handleComplete = () => {
    // 사용자 정보 처리 후 메인 페이지로 이동
    console.log("이름:", name, "성별:", gender);
    // 실제 구현에서는 메인 페이지로의 내비게이션 로직을 추가해야 합니다.
  };

  return (
    <div>
      <Dialog open={showFirstModal}>
        <DialogTrigger asChild>
          <Button onClick={() => setShowFirstModal(true)}>모달 열기</Button>
        </DialogTrigger>
        <DialogContent>
          <Label htmlFor="name">이름</Label>
          <Input
            id="name"
            placeholder="이름을 입력하세요"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />
          <Label htmlFor="gender">성별</Label>
          <Select onValueChange={setGender}>
            <SelectTrigger>
              <span>{gender || "성별 선택"}</span>
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="male">남성</SelectItem>
              <SelectItem value="female">여성</SelectItem>
            </SelectContent>
          </Select>
          <Button onClick={handleNext}>완료</Button>
        </DialogContent>
      </Dialog>

      <Dialog open={showSecondModal}>
        <DialogContent>
          <Label htmlFor="search">검색어 입력</Label>
          <Input
            id="search"
            placeholder="검색어를 입력하세요"
            // 자동 완성 처리 로직을 추가해야 합니다.
          />
          <Button onClick={handleComplete}>완료</Button>
        </DialogContent>
      </Dialog>

      <MainPage />
    </div>
  );
};

export default ModalFlow;
