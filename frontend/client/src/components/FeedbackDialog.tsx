import { useState } from "react";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { MessageSquarePlus, Send, Loader2 } from "lucide-react";
import { toast } from "sonner";

export function FeedbackDialog() {
  const [open, setOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    message: ""
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    // 模拟提交延迟
    await new Promise(resolve => setTimeout(resolve, 1000));

    // 构建邮件链接
    const subject = encodeURIComponent(`ThinkDeep.ai 用户反馈 - ${formData.name}`);
    const body = encodeURIComponent(`发送者: ${formData.name} (${formData.email})\n\n反馈内容:\n${formData.message}`);
    const mailtoLink = `mailto:chenysh48@foxmail.com?subject=${subject}&body=${body}`;

    // 唤起邮件客户端
    window.location.href = mailtoLink;

    toast.success("感谢您的反馈！正在唤起邮件客户端...");
    setLoading(false);
    setOpen(false);
    setFormData({ name: "", email: "", message: "" });
  };

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button 
          variant="outline" 
          className="w-full justify-start gap-2 border-2 border-black hover:bg-gray-100 rounded-none transition-all shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] hover:translate-x-[-1px] hover:translate-y-[-1px] hover:shadow-[3px_3px_0px_0px_rgba(0,0,0,1)]"
        >
          <MessageSquarePlus className="w-4 h-4" />
          意见反馈
        </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[425px] border-2 border-black shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] rounded-none p-6">
        <DialogHeader>
          <DialogTitle className="text-xl font-bold font-heading">意见反馈</DialogTitle>
          <DialogDescription className="text-gray-500">
            您的建议是我们进步的动力。请告诉我们您的想法，或报告您遇到的问题。
          </DialogDescription>
        </DialogHeader>
        <form onSubmit={handleSubmit} className="grid gap-4 py-4">
          <div className="grid gap-2">
            <Label htmlFor="name" className="font-bold">称呼</Label>
            <Input
              id="name"
              placeholder="怎么称呼您"
              className="rounded-none border-2 border-black focus-visible:ring-0 focus-visible:ring-offset-0 focus-visible:border-blue-600"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              required
            />
          </div>
          <div className="grid gap-2">
            <Label htmlFor="email" className="font-bold">联系邮箱</Label>
            <Input
              id="email"
              type="email"
              placeholder="your@email.com"
              className="rounded-none border-2 border-black focus-visible:ring-0 focus-visible:ring-offset-0 focus-visible:border-blue-600"
              value={formData.email}
              onChange={(e) => setFormData({ ...formData, email: e.target.value })}
              required
            />
          </div>
          <div className="grid gap-2">
            <Label htmlFor="message" className="font-bold">反馈内容</Label>
            <Textarea
              id="message"
              placeholder="请详细描述您的建议或问题..."
              className="min-h-[100px] rounded-none border-2 border-black focus-visible:ring-0 focus-visible:ring-offset-0 focus-visible:border-blue-600 resize-none"
              value={formData.message}
              onChange={(e) => setFormData({ ...formData, message: e.target.value })}
              required
            />
          </div>
          <DialogFooter className="mt-4">
            <Button 
              type="submit" 
              disabled={loading}
              className="w-full bg-black text-white hover:bg-gray-800 rounded-none border-2 border-transparent hover:border-black transition-all"
            >
              {loading ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  处理中...
                </>
              ) : (
                <>
                  <Send className="mr-2 h-4 w-4" />
                  发送反馈
                </>
              )}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}
